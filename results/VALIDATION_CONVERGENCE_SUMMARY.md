# Draft 3 Validation Convergence Summary

The 48 Draft 3 searches completed 50 trials each. This audit uses validation RMSE only; no test result entered the calculation.

| Specification | Mean best RMSE at 10 | at 25 | at 50 | Mean change 10 to 25 | Mean change 25 to 50 | Searches improving after 25 | Same best trial at 25 and 50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| catboost_local_only | 15.5348 | 15.4500 | 15.3954 | -0.0848 | -0.0546 | 16 / 24 | 8 / 24 |
| catboost_local_plus_merra | 15.4150 | 15.3422 | 15.2938 | -0.0728 | -0.0485 | 14 / 24 | 10 / 24 |

Negative changes indicate lower validation RMSE at the later checkpoint.
The 50-trial search was used for Draft 3 model selection. The checkpoint results are descriptive convergence evidence, not additional model selections.
