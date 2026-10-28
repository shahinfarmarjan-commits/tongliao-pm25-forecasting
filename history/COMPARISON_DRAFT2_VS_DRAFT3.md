# Draft 2 versus Draft 3 Comparison

Draft 3 uses 50 validation-only Optuna trials per search and the same historical test period as Draft 2. It is therefore a revised reanalysis, not independent external validation.

## Overall primary metrics

| Version | Model | Mean R2 | Mean RMSE | Mean MAE | Mean bias |
|---|---|---:|---:|---:|---:|
| Draft 2 | catboost_local_only | 0.4060 | 23.285 | 15.362 | -0.066 |
| Draft 2 | catboost_local_plus_merra | 0.4473 | 22.512 | 15.195 | 1.797 |
| Draft 3 | catboost_local_only | 0.4125 | 23.142 | 15.331 | 0.099 |
| Draft 3 | catboost_local_plus_merra | 0.4563 | 22.323 | 15.061 | 1.846 |

## Horizon bands

| Version | Band | Local R2 | Full R2 | Full minus local delta R2 |
|---|---|---:|---:|---:|
| Draft 2 | h1-h6 | 0.7484 | 0.7474 | -0.0011 |
| Draft 3 | h1-h6 | 0.7517 | 0.7508 | -0.0009 |
| Draft 2 | h7-h12 | 0.4006 | 0.4414 | +0.0409 |
| Draft 3 | h7-h12 | 0.3984 | 0.4506 | +0.0522 |
| Draft 2 | h13-h24 | 0.2376 | 0.3001 | +0.0625 |
| Draft 3 | h13-h24 | 0.2500 | 0.3120 | +0.0620 |
| Draft 2 | h1-h24 | 0.4060 | 0.4473 | +0.0412 |
| Draft 3 | h1-h24 | 0.4125 | 0.4563 | +0.0438 |

## Interpretation

Draft 3 modestly improves average validation-selected test performance for both specifications. The main horizon-dependent pattern is preserved: MERRA-2 adds little average R2 at h1-h6 and more at h7-h12 and h13-h24. Individual horizons do not all improve; the paper must report the full horizon table rather than implying universal benefit.

The h24 result remains an important exception to the broad pattern and must be described from the Draft 3 table rather than generalized away.
