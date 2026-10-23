# Step 9: Optuna and One-Time Locked-Test Evaluation

Status: **PASS / COMPLETE / PARAMETERS LOCKED**

## Primary mean h1-h24 locked-test performance

| Model | R2 | RMSE | MAE | Bias |
|---|---:|---:|---:|---:|
| Persistence | -0.0009 | 30.335 | 19.410 | -0.312 |
| Month-hour climatology | 0.1550 | 28.524 | 20.063 | 1.155 |
| Tuned local-only CatBoost (149) | 0.4060 | 23.285 | 15.362 | -0.066 |
| Tuned local + MERRA-2 CatBoost (222) | 0.4473 | 22.512 | 15.195 | 1.797 |

## Corrected MERRA-2 contribution

- Mean h1-h24 R2: `0.4060 -> 0.4473` (`+0.0412`).
- Mean RMSE difference: `-0.772 ug/m3`.
- Mean MAE difference: `-0.167 ug/m3`.
- MERRA improves R2 and RMSE at `21/24` horizons and MAE at `15/24`.

## Horizon bands

| Band | Local R2 | Local + MERRA R2 | Delta |
|---|---:|---:|---:|
| h1-h6 | 0.7484 | 0.7474 | -0.0011 |
| h7-h12 | 0.4006 | 0.4414 | +0.0409 |
| h13-h24 | 0.2376 | 0.3001 | +0.0625 |

MERRA provides little short-horizon benefit and slightly lowers mean h1-h6 R2. Its contribution is concentrated at transition and longer horizons. This pattern is reported as observed; no post-test model switching or retuning is permitted.

## Sensitivity stability

The four MERRA scenarios have very similar mean h1-h24 test performance. The retrospective combined nearest-cell/hour-start scenario has the highest numerical R2, but it was not selected because primary and sensitivity roles were frozen before modeling.

## Integrity

- 48 Optuna studies, 10 completed trials each: 480 completed trials.
- One interrupted trial from the controlled thread-count restart is retained as FAIL.
- Test data were opened only after all primary studies and parameter selections completed.
- Local-only and MERRA models were tuned separately using training/validation only.
- Sensitivity scenarios reused locked primary MERRA parameters.
- Evaluation used uncapped observed PM2.5.
- No post-test retuning or model selection was performed.

MERRA-enhanced results are retrospective forecasting unless product-delivery latency is represented.
