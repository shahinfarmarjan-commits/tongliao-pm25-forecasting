# Scientific Status Record

## Draft 3 primary design

- Study period: 1 January 2020 through 31 December 2021.
- Hourly monitoring timestamps: 17,544.
- Forecast horizons: h1 through h24.
- Locked-test targets: 3,373 per horizon.
- Primary comparison: 149-predictor local-only versus 222-predictor local plus MERRA-2.
- The 222-predictor model includes 73 MERRA-2 predictors.
- Rows were partitioned chronologically by target time.
- There were 48 validation-only Optuna searches, each with 50 completed trials, for 2,400 completed trials total. Each search used 20 startup trials before adaptive TPE.

## Draft 3 primary results

| Model | Mean R2, h1-h24 | Mean RMSE | Mean MAE |
|---|---:|---:|---:|
| Persistence | -0.0009 | 30.335 | 19.410 |
| Month-hour climatology | 0.1550 | 28.524 | 20.063 |
| Local-only CatBoost | 0.4125 | 23.142 | 15.331 |
| Local plus MERRA-2 CatBoost | 0.4563 | 22.323 | 15.061 |

At h1, full-model R2 was 0.9488. At h24, full-model R2 was 0.2044 and local-only R2 was 0.2102. The paired gap-aware interval included zero at h24.

## Horizon pattern

- Mean delta R2 was -0.0009 at h1-h6.
- Mean delta R2 was +0.0522 at h7-h12.
- Mean delta R2 was +0.0620 at h13-h24.
- The full model had higher R2 at 22 of 24 horizons; this is not universal improvement.

## Secondary evidence

Seasonal, SHAP, ablation, feature-reduction, pressure, and fixed-setting analyses are identified in the Draft 3 manuscript as retained secondary evidence when their original protocol was not rerun after retuning. The historical Draft 2 SHAP and ablation values are not presented as Draft 3 primary re-estimates.

## Warning results

- Draft 3 mean P90 F1: 0.301 full and 0.203 local-only.
- Draft 3 mean P95 recall: 0.099 full and 0.090 local-only.
- Rare-event warnings require prospective validation.

## Open limitations

- MERRA-2 delivery latency was not modeled.
- Mine-operation variables were unavailable.
- The primary test is historical and not external validation.
- Prospective new-period and external-mine validation remain necessary.
