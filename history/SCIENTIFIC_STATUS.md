# Scientific Status Record

## Dataset and design

- Study period: 1 January 2020 through 31 December 2021.
- Hourly monitoring timestamps: 17,544.
- Forecast horizons: h1 through h24.
- Locked-test targets: 3,373 per horizon.
- Primary model comparison: 149-predictor local-only versus 222-predictor local plus MERRA-2.
- The 222-predictor model includes 73 MERRA-2 predictors.
- Rows were partitioned chronologically by target time.

## Primary results

| Model | Mean R2, h1-h24 | Mean RMSE | Mean MAE |
|---|---:|---:|---:|
| Persistence | -0.0009 | 30.335 | 19.410 |
| Month-hour climatology | 0.1550 | 28.524 | 20.063 |
| Local-only CatBoost | 0.4060 | 23.285 | 15.362 |
| Local plus MERRA-2 CatBoost | 0.4473 | 22.512 | 15.195 |

At h1, the full-model R2 was 0.9428. At h24, full-model R2 was 0.2320 and local-only R2 was 0.2437; the paired interval included zero.

## Interpretation

- MERRA-2 added little average value at h1-h6.
- Average value was clearer at h7-h12 and h13-h24.
- MERRA-2 SHAP attribution increased from 5.3% at h1 to 32.3% at h24.
- Recent pollutant-history attribution decreased from 63.6% at h1 to 20.1% at h24.
- These are model attribution and predictive comparisons, not causal evidence.

## Seasonal and warning results

- Winter mean PM2.5: 51.5 ug m-3.
- Summer mean PM2.5: 22.7 ug m-3.
- Seasonal delta R2: spring +0.0043, summer +0.0203, autumn +0.0481, composite winter -0.0024.
- Full-model mean P90 F1: 0.293.
- Local-only mean P90 F1: 0.197.
- Full-model P95 recall: 0.095.

## Model-selection boundary

- There were 48 Optuna searches: 24 horizons x 2 predictor sets.
- Each search used 10 completed trials, for 480 completed trials.
- The 10 trials were startup trials; adaptive TPE did not begin.
- The 59-predictor candidate was post-hoc, validation-only, and was not evaluated on the locked test.

## Open limitations

- MERRA-2 delivery latency was not modeled.
- The monitoring source does not provide fully verified station provenance.
- Mine-operation variables were unavailable.
- The original main-test bootstrap treated rows as sequential and could cross missing calendar-hour gaps.
- The corrected pressure pipeline was examined on validation data only.
- Prospective new-period and external-mine validation remain necessary.
