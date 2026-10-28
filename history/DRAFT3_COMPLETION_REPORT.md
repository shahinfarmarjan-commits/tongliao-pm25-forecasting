# Draft 3 Completion Report

## Status

Draft 3 is complete as a primary-results reanalysis package. Draft 2 was frozen and left unchanged.

## Completed gates

1. Draft 2 was copied into an isolated Draft 3 workspace and hashed.
2. The 50-trial amendment was recorded before execution.
3. The h1 smoke test passed for both 149- and 222-predictor specifications.
4. All 48 searches completed 50 validation-only trials, giving 2,400 completed trials.
5. Convergence checkpoints were saved at trials 10, 25, and 50.
6. The historical locked test was scored only after tuning completed.
7. Primary metrics were regenerated for h1–h24, including R², RMSE, MAE, bias, and sample count.
8. Draft 3 horizon-band comparisons and gap-aware uncertainty intervals were generated.
9. Draft 3 warning means were regenerated from the new primary predictions.
10. The manuscript, supplementary tables, captions, and primary figures were updated.
11. PDF renders passed text, page-count, stale-number, and artifact checks.
12. The public GitHub release was updated and superseded 10-trial artifacts were removed.

## Draft 2 versus Draft 3

| Specification | Draft 2 mean R² | Draft 3 mean R² | Draft 2 mean RMSE | Draft 3 mean RMSE |
|---|---:|---:|---:|---:|
| Local-only | 0.4060 | 0.4125 | 23.285 | 23.142 |
| Local + MERRA-2 | 0.4473 | 0.4563 | 22.512 | 22.323 |

Draft 3 preserved the central horizon pattern. Mean ΔR² was −0.0009 at h1–h6, +0.0522 at h7–h12, and +0.0620 at h13–h24. The full model was better in R² at 22 of 24 horizons, but not at every horizon. At h24, full-model R² was 0.2044 and local-only R² was 0.2102.

## Scope note

Seasonal, SHAP, input-group removal, feature-reduction, pressure, and fixed-setting analyses remain separately scoped secondary evidence when their original protocol was not rerun after retuning. No partial SHAP output is included. This preserves a clear distinction between Draft 3 primary metrics and retained Draft 2 secondary evidence.

Draft 3 uses the same historical test period as Draft 2 and is not independent external validation.
