from __future__ import annotations
import json,math
import os
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.metrics import r2_score

PROJECT_ROOT=os.environ.get("TONGLIAO_PROJECT_ROOT")
if not PROJECT_ROOT:
    raise RuntimeError("Set TONGLIAO_PROJECT_ROOT to the local project root before running this script.")
ROOT=Path(PROJECT_ROOT);OUT=ROOT/"05_evaluation_shap"/"block_bootstrap_uncertainty";OUT.mkdir(parents=True,exist_ok=True)
MAIN=ROOT/"04_model_training"/"step9_optuna_locked_test"/"locked_test_predictions_h1_h24.parquet"
SEASONAL=ROOT/"05_evaluation_shap"/"corrected_four_season_rolling_origin"/"tables"/"09_predictions_all_seasons_h1_h24.parquet"
MAIN_EVENTS=ROOT/"05_evaluation_shap"/"step10_repeated_scientific_analyses"/"tables"/"03_high_pollution_warning_performance.csv"
SEASON_EVENTS=ROOT/"05_evaluation_shap"/"corrected_four_season_rolling_origin"/"tables"/"03_event_metrics.csv"
B=1000;BLOCK=28;SEED=42

def indices(n,rng):
 starts=rng.integers(0,n,size=math.ceil(n/BLOCK));return np.concatenate([(s+np.arange(BLOCK))%n for s in starts])[:n]
def reg(y,p):
 return {"R2":r2_score(y,p),"RMSE":np.sqrt(np.mean((p-y)**2)),"MAE":np.mean(np.abs(p-y)),"bias":np.mean(p-y)}
def evt(y,p,t):
 o=y>=t;q=p>=t;tp=np.sum(o&q);fp=np.sum(~o&q);fn=np.sum(o&~q)
 precision=tp/(tp+fp) if tp+fp else 0.;recall=tp/(tp+fn) if tp+fn else 0.;f1=2*precision*recall/(precision+recall) if precision+recall else 0.
 return {"precision":precision,"recall":recall,"F1":f1}
def add_ci(rows,scope,season,horizon,comparison,metric,point,samples):
 rows.append({"scope":scope,"season":season,"horizon_h":horizon,"comparison":comparison,"metric":metric,"point_estimate":point,"ci_lower":np.percentile(samples,2.5),"ci_upper":np.percentile(samples,97.5),"bootstrap_replicates":B,"block_length_h":BLOCK})
def process(data,scope,event_table,season_col):
 rows=[];rng=np.random.default_rng(SEED+(0 if scope=='main_locked_test' else 1000))
 group_cols=([season_col] if season_col else [])+["horizon_h"]
 for keys,g in data.groupby(group_cols,sort=True):
  if not isinstance(keys,tuple):keys=(keys,)
  season=keys[0] if season_col else "All";h=int(keys[-1]);pivot=g.pivot_table(index=["origin_time","target_time","observed_pm25_uncapped"],columns="model",values="prediction",aggfunc="first").reset_index().sort_values("target_time")
  y=pivot.observed_pm25_uncapped.to_numpy(float);local=pivot.catboost_local_only.to_numpy(float);merra=pivot.catboost_local_plus_merra.to_numpy(float);n=len(y)
  samples={f"{model}_{metric}":[] for model in ['local','merra'] for metric in ['R2','RMSE','MAE','bias']};samples.update({f"delta_{m}":[] for m in ['R2','RMSE','MAE']})
  thresholds={}
  sub=event_table[event_table.horizon_h.eq(h)]
  if season_col:sub=sub[sub.season.eq(season)]
  for rule in ['top10_train_p90','top5_train_p95']:thresholds[rule]=float(sub[sub.threshold_rule.eq(rule)].threshold.iloc[0])
  event_samples={(model,rule,m):[] for model in ['local','merra'] for rule in thresholds for m in ['precision','recall','F1']}
  for _ in range(B):
   idx=indices(n,rng);yb,lb,mb=y[idx],local[idx],merra[idx];lr,mr=reg(yb,lb),reg(yb,mb)
   for metric in lr:samples[f"local_{metric}"].append(lr[metric]);samples[f"merra_{metric}"].append(mr[metric])
   for metric in ['R2','RMSE','MAE']:samples[f"delta_{metric}"].append(mr[metric]-lr[metric])
   for rule,t in thresholds.items():
    for model,p in [('local',lb),('merra',mb)]:
     e=evt(yb,p,t)
     for metric,value in e.items():event_samples[(model,rule,metric)].append(value)
  lp,mp=reg(y,local),reg(y,merra)
  for model,point in [('local',lp),('merra',mp)]:
   for metric,value in point.items():add_ci(rows,scope,season,h,model,metric,value,samples[f"{model}_{metric}"])
  for metric in ['R2','RMSE','MAE']:add_ci(rows,scope,season,h,'merra_minus_local',metric,mp[metric]-lp[metric],samples[f"delta_{metric}"])
  for rule,t in thresholds.items():
   for model,p in [('local',local),('merra',merra)]:
    point=evt(y,p,t)
    for metric,value in point.items():add_ci(rows,scope,season,h,f"{model}_{rule}",metric,value,event_samples[(model,rule,metric)])
 return pd.DataFrame(rows)

def main():
 main=pd.read_parquet(MAIN);main=main[(main.scenario=='primary_causal_area_weighted_cst_hour_end')&main.model.isin(['catboost_local_only','catboost_local_plus_merra'])]
 seasonal=pd.read_parquet(SEASONAL);seasonal=seasonal[seasonal.model.isin(['catboost_local_only','catboost_local_plus_merra'])]
 result=pd.concat([process(main,'main_locked_test',pd.read_csv(MAIN_EVENTS),None),process(seasonal,'seasonal_rolling_origin',pd.read_csv(SEASON_EVENTS),'season')],ignore_index=True)
 result.to_csv(OUT/'block_bootstrap_confidence_intervals.csv',index=False)
 with pd.ExcelWriter(OUT/'block_bootstrap_confidence_intervals.xlsx',engine='openpyxl') as w:result.to_excel(w,index=False,sheet_name='confidence_intervals')
 assertions={"status":"PASS","replicates":B,"block_length_h":BLOCK,"main_horizons":result[result.scope=='main_locked_test'].horizon_h.nunique(),"seasonal_cells":result[result.scope=='seasonal_rolling_origin'].groupby(['season','horizon_h']).ngroups,"rows":len(result),"finite_intervals":bool(np.isfinite(result[['point_estimate','ci_lower','ci_upper']]).all().all())}
 if assertions['main_horizons']!=24 or assertions['seasonal_cells']!=96 or not assertions['finite_intervals']:raise AssertionError(assertions)
 (OUT/'ASSERTIONS.json').write_text(json.dumps(assertions,indent=2),encoding='utf-8');print(json.dumps(assertions,indent=2))
if __name__=='__main__':main()
