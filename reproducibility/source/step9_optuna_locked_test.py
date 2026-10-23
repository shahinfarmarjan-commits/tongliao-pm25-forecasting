from __future__ import annotations

import hashlib
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import optuna
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


PROJECT_ROOT = os.environ.get("TONGLIAO_PROJECT_ROOT")
if not PROJECT_ROOT:
    raise RuntimeError("Set TONGLIAO_PROJECT_ROOT to the local project root before running this script.")
ROOT = Path(PROJECT_ROOT)
STEP6 = ROOT / "02_preprocessing" / "step6_leakage_controlled_inputs"
STEP7 = ROOT / "03_feature_engineering" / "step7_rebuilt_features"
OUTPUT = ROOT / "04_model_training" / "step9_optuna_locked_test"
STUDY_DIR = OUTPUT / "studies"

PRIMARY = "primary_causal_area_weighted_cst_hour_end"
SCENARIOS = {
    PRIMARY: STEP7 / f"{PRIMARY}_origin_features.parquet",
    "causal_spatial_sensitivity_nearest_cell_cst_hour_end": STEP7 / "causal_spatial_sensitivity_nearest_cell_cst_hour_end_origin_features.parquet",
    "retrospective_timing_sensitivity_area_weighted_cst_hour_start": STEP7 / "retrospective_timing_sensitivity_area_weighted_cst_hour_start_origin_features.parquet",
    "retrospective_combined_sensitivity_nearest_cell_cst_hour_start": STEP7 / "retrospective_combined_sensitivity_nearest_cell_cst_hour_start_origin_features.parquet",
}
TARGET_PATH = STEP7 / "h1_h24_target_calendar_and_uncapped_targets.parquet"
FAMILY_PATH = STEP7 / "corrected_feature_family_map.csv"
RAW_ORIGIN_PATH = STEP6 / "primary_causal_area_weighted_cst_hour_end_step6_hourly_inputs.parquet"

SEED = 42
N_TRIALS = 10
THREADS = 8
TARGET_FEATURES = [
    "target_hour_sin", "target_hour_cos", "target_doy_sin", "target_doy_cos",
    "target_day_of_year", "target_month_sin", "target_month_cos",
    "target_is_winter", "target_is_heating_season",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metrics(y_true: np.ndarray, prediction: np.ndarray) -> dict[str, float | int]:
    valid = np.isfinite(y_true) & np.isfinite(prediction)
    y_true, prediction = y_true[valid], prediction[valid]
    return {
        "R2": float(r2_score(y_true, prediction)),
        "RMSE": float(math.sqrt(mean_squared_error(y_true, prediction))),
        "MAE": float(mean_absolute_error(y_true, prediction)),
        "bias": float(np.mean(prediction - y_true)),
        "n": int(len(y_true)),
    }


def assemble(origin: pd.DataFrame, horizon: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    origin_columns = [feature for feature in features if feature in origin.columns]
    target_columns = [feature for feature in features if feature in horizon.columns]
    missing = sorted(set(features) - set(origin_columns) - set(target_columns))
    if missing:
        raise AssertionError(f"Unavailable features: {missing}")
    merged = horizon.merge(origin[["origin_time"] + origin_columns], on="origin_time", how="left", validate="many_to_one")
    return merged


def catboost_params(trial: optuna.Trial) -> dict:
    return {
        "iterations": trial.suggest_int("iterations", 250, 1000),
        "depth": trial.suggest_int("depth", 4, 8),
        "learning_rate": trial.suggest_float("learning_rate", 0.015, 0.18, log=True),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1.0, 25.0, log=True),
        "random_strength": trial.suggest_float("random_strength", 0.0, 5.0),
        "bagging_temperature": trial.suggest_float("bagging_temperature", 0.0, 5.0),
        "border_count": trial.suggest_int("border_count", 64, 254),
        "loss_function": "RMSE",
        "eval_metric": "RMSE",
        "random_seed": SEED,
        "verbose": False,
        "allow_writing_files": False,
        "thread_count": THREADS,
    }


def tune_study(model_name: str, horizon: int, frame: pd.DataFrame, features: list[str]) -> tuple[dict, pd.DataFrame]:
    train = frame.loc[frame["eligible"] & frame["split"].eq("train")]
    validation = frame.loc[frame["eligible"] & frame["split"].eq("validation")]
    if frame["split"].eq("test").any():
        raise AssertionError("Test rows entered tuning frame")
    database = STUDY_DIR / f"{model_name}_h{horizon:02d}.sqlite3"
    study_name = f"step9_{model_name}_h{horizon:02d}"
    study = optuna.create_study(
        study_name=study_name,
        storage=f"sqlite:///{database.as_posix()}",
        direction="minimize",
        sampler=optuna.samplers.TPESampler(seed=SEED),
        load_if_exists=True,
    )

    def objective(trial: optuna.Trial) -> float:
        params = catboost_params(trial)
        model = CatBoostRegressor(**params)
        started = time.perf_counter()
        model.fit(
            train[features],
            train["evaluation_target_pm25_uncapped"],
            eval_set=(validation[features], validation["evaluation_target_pm25_uncapped"]),
            early_stopping_rounds=50,
            verbose=False,
        )
        prediction = model.predict(validation[features])
        score = math.sqrt(mean_squared_error(validation["evaluation_target_pm25_uncapped"], prediction))
        best_iteration = model.get_best_iteration()
        trial.set_user_attr("best_iteration", int(best_iteration if best_iteration is not None and best_iteration >= 0 else params["iterations"] - 1))
        trial.set_user_attr("fit_seconds", float(time.perf_counter() - started))
        return float(score)

    completed = len([trial for trial in study.trials if trial.state == optuna.trial.TrialState.COMPLETE])
    if completed < N_TRIALS:
        study.optimize(objective, n_trials=N_TRIALS - completed, show_progress_bar=False, gc_after_trial=True)
    completed = len([trial for trial in study.trials if trial.state == optuna.trial.TrialState.COMPLETE])
    if completed < N_TRIALS:
        raise AssertionError(f"{study_name}: only {completed}/{N_TRIALS} complete trials")

    best = study.best_trial
    final = dict(best.params)
    final["iterations"] = max(50, int(best.user_attrs["best_iteration"]) + 1)
    final.update({
        "loss_function": "RMSE", "eval_metric": "RMSE", "random_seed": SEED,
        "verbose": False, "allow_writing_files": False, "thread_count": THREADS,
    })
    trials = study.trials_dataframe(attrs=("number", "value", "params", "user_attrs", "state"))
    trials.insert(0, "horizon_h", horizon)
    trials.insert(0, "model", model_name)
    return final, trials


def climatology(trainval: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
    trainval = trainval.copy(); test = test.copy()
    for frame in [trainval, test]:
        frame["month"] = pd.to_datetime(frame["target_time"]).dt.month
        frame["hour"] = pd.to_datetime(frame["target_time"]).dt.hour
    means = trainval.groupby(["month", "hour"])["evaluation_target_pm25_uncapped"].mean()
    monthly = trainval.groupby("month")["evaluation_target_pm25_uncapped"].mean()
    global_mean = float(trainval["evaluation_target_pm25_uncapped"].mean())
    return np.asarray([means.get((row.month, row.hour), monthly.get(row.month, global_mean)) for row in test.itertuples(index=False)], dtype=float)


def main() -> None:
    started = datetime.now(timezone.utc)
    OUTPUT.mkdir(parents=True, exist_ok=True); STUDY_DIR.mkdir(parents=True, exist_ok=True)
    progress = OUTPUT / "progress.txt"
    family = pd.read_csv(FAMILY_PATH)
    all_features = family["feature_name"].tolist()
    merra = set(family.loc[family["feature_family"].eq("MERRA-2 aerosol/reanalysis"), "feature_name"])
    local_features = [feature for feature in all_features if feature not in merra]
    primary_origin = pd.read_parquet(SCENARIOS[PRIMARY])
    origin_names = set(primary_origin.columns) - {"origin_time"}
    local = [feature for feature in local_features if feature in origin_names] + TARGET_FEATURES
    full = [feature for feature in all_features if feature in origin_names] + TARGET_FEATURES
    if len(local) != 149 or len(full) != 222:
        raise AssertionError("Feature counts differ from frozen contract")

    target = pd.read_parquet(TARGET_PATH)
    tuning_target = target.loc[~target["split"].eq("test")].copy()
    if tuning_target["split"].eq("test").any():
        raise AssertionError("Test lock failed before tuning")

    best_rows = []
    all_trials = []
    selected: dict[tuple[str, int], dict] = {}
    total_studies = 48
    completed_studies = 0
    for horizon in range(1, 25):
        horizon_target = tuning_target.loc[tuning_target["horizon_h"].eq(horizon)]
        for model_name, features in [("catboost_local_only", local), ("catboost_local_plus_merra", full)]:
            frame = assemble(primary_origin, horizon_target, features)
            params, trials = tune_study(model_name, horizon, frame, features)
            selected[(model_name, horizon)] = params
            all_trials.append(trials)
            best_rows.append({"model": model_name, "horizon_h": horizon, **params})
            completed_studies += 1
            pd.DataFrame(best_rows).to_csv(OUTPUT / "selected_hyperparameters_partial.csv", index=False)
            progress.write_text(f"TUNING {completed_studies}/{total_studies} studies complete; {model_name}; h={horizon}\n", encoding="utf-8")

    trials_frame = pd.concat(all_trials, ignore_index=True)
    trials_frame.to_csv(OUTPUT / "optuna_trials_all.csv", index=False)
    params_frame = pd.DataFrame(best_rows)
    params_frame.to_csv(OUTPUT / "selected_hyperparameters_h1_h24.csv", index=False)
    completed_by_study = (
        trials_frame.loc[trials_frame["state"].astype(str).eq("COMPLETE")]
        .groupby(["model", "horizon_h"])
        .size()
    )
    if len(params_frame) != 48 or len(completed_by_study) != 48 or completed_by_study.min() < N_TRIALS:
        raise AssertionError("Tuning completion assertion failed")

    # Hard phase boundary: only now create test scoring frames.
    test_target = target.loc[target["split"].eq("test")].copy()
    raw_origin = pd.read_parquet(RAW_ORIGIN_PATH)[["time", "pm25"]].rename(columns={"time": "origin_time", "pm25": "origin_pm25_uncapped"})
    scenario_origins = {scenario: pd.read_parquet(path) for scenario, path in SCENARIOS.items()}
    metric_rows = []; prediction_parts = []; final_fits = 0
    for horizon in range(1, 25):
        horizon_all = target.loc[target["horizon_h"].eq(horizon)]
        # Context baselines.
        base = horizon_all.merge(raw_origin, on="origin_time", how="left", validate="one_to_one")
        trainval_base = base.loc[base["eligible"] & base["split"].isin(["train", "validation"])]
        test_base = base.loc[base["eligible"] & base["split"].eq("test")]
        y_test = test_base["evaluation_target_pm25_uncapped"].to_numpy(float)
        for name, prediction in [
            ("persistence", test_base["origin_pm25_uncapped"].to_numpy(float)),
            ("month_hour_climatology", climatology(trainval_base, test_base)),
        ]:
            metric_rows.append({"scenario": PRIMARY, "model": name, "horizon_h": horizon, "evaluation_split": "test", **metrics(y_test, prediction)})
            prediction_parts.append(pd.DataFrame({"scenario": PRIMARY, "model": name, "horizon_h": horizon, "origin_time": test_base["origin_time"], "target_time": test_base["target_time"], "observed_pm25_uncapped": y_test, "prediction": prediction}))

        # Primary local-only and MERRA.
        for model_name, features in [("catboost_local_only", local), ("catboost_local_plus_merra", full)]:
            frame = assemble(primary_origin, horizon_all, features)
            trainval = frame.loc[frame["eligible"] & frame["split"].isin(["train", "validation"])]
            test = frame.loc[frame["eligible"] & frame["split"].eq("test")]
            model = CatBoostRegressor(**selected[(model_name, horizon)])
            model.fit(trainval[features], trainval["evaluation_target_pm25_uncapped"])
            prediction = model.predict(test[features]); final_fits += 1
            metric_rows.append({"scenario": PRIMARY, "model": model_name, "horizon_h": horizon, "evaluation_split": "test", "feature_count": len(features), **metrics(test["evaluation_target_pm25_uncapped"].to_numpy(float), prediction)})
            prediction_parts.append(pd.DataFrame({"scenario": PRIMARY, "model": model_name, "horizon_h": horizon, "origin_time": test["origin_time"], "target_time": test["target_time"], "observed_pm25_uncapped": test["evaluation_target_pm25_uncapped"], "prediction": prediction}))

        # Sensitivities reuse locked primary MERRA parameters.
        for scenario, origin in scenario_origins.items():
            if scenario == PRIMARY: continue
            frame = assemble(origin, horizon_all, full)
            trainval = frame.loc[frame["eligible"] & frame["split"].isin(["train", "validation"])]
            test = frame.loc[frame["eligible"] & frame["split"].eq("test")]
            model = CatBoostRegressor(**selected[("catboost_local_plus_merra", horizon)])
            model.fit(trainval[full], trainval["evaluation_target_pm25_uncapped"])
            prediction = model.predict(test[full]); final_fits += 1
            metric_rows.append({"scenario": scenario, "model": "catboost_local_plus_merra", "horizon_h": horizon, "evaluation_split": "test", "feature_count": len(full), **metrics(test["evaluation_target_pm25_uncapped"].to_numpy(float), prediction)})
            prediction_parts.append(pd.DataFrame({"scenario": scenario, "model": "catboost_local_plus_merra", "horizon_h": horizon, "origin_time": test["origin_time"], "target_time": test["target_time"], "observed_pm25_uncapped": test["evaluation_target_pm25_uncapped"], "prediction": prediction}))
        progress.write_text(f"TEST {horizon}/24 horizons complete\n", encoding="utf-8")

    metrics_frame = pd.DataFrame(metric_rows); predictions = pd.concat(prediction_parts, ignore_index=True)
    metrics_frame.to_csv(OUTPUT / "locked_test_metrics_h1_h24.csv", index=False)
    predictions.to_parquet(OUTPUT / "locked_test_predictions_h1_h24.parquet", index=False)
    bands = []
    for (scenario, model), group in metrics_frame.groupby(["scenario", "model"], sort=False):
        for band, low, high in [("h1-h6",1,6),("h7-h12",7,12),("h13-h24",13,24),("h1-h24",1,24)]:
            subset=group[group.horizon_h.between(low,high)]
            bands.append({"scenario":scenario,"model":model,"band":band,"mean_R2":subset.R2.mean(),"mean_RMSE":subset.RMSE.mean(),"mean_MAE":subset.MAE.mean(),"mean_bias":subset.bias.mean(),"horizons":subset.horizon_h.nunique()})
    pd.DataFrame(bands).to_csv(OUTPUT / "locked_test_horizon_band_summary.csv", index=False)
    assertions = {"status":"PASS","optuna_studies":48,"trials_per_study":10,"completed_trials":int((trials_frame["state"].astype(str)=="COMPLETE").sum()),"historical_noncomplete_trials":int((trials_frame["state"].astype(str)!="COMPLETE").sum()),"test_opened_after_all_studies":True,"primary_final_fits":48,"sensitivity_final_fits":72,"total_final_catboost_fits":final_fits,"uncapped_test_targets":True,"sensitivity_tuned_separately":False}
    (OUTPUT / "STEP9_ASSERTIONS.json").write_text(json.dumps(assertions,indent=2),encoding="utf-8")
    manifest={"label":"STEP 9 OPTUNA + ONE-TIME LOCKED TEST","started_utc":started.isoformat(),"finished_utc":datetime.now(timezone.utc).isoformat(),"protocol":str(ROOT/'07_run_control/STEP9_OPTUNA_PROTOCOL_2026-08-13.md'),"seed":SEED,"n_trials":N_TRIALS,"assertions":assertions,"inputs":{k:{"path":str(v),"sha256":sha256(v)} for k,v in SCENARIOS.items()},"target_sha256":sha256(TARGET_PATH),"interpretation":"MERRA-enhanced models are retrospective forecasting unless delivery latency is modeled."}
    (OUTPUT / "STEP9_MANIFEST.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    progress.write_text("DONE\n",encoding="utf-8")


if __name__ == "__main__":
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    main()
