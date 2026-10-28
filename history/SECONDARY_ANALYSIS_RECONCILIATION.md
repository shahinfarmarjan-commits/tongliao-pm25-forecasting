# Draft 3 Secondary-Analysis Reconciliation

Draft 3 changed the primary CatBoost tuning budget from 10 to 50 validation-only trials per search and regenerated the primary locked-test predictions. The primary results, horizon-band comparisons, warning means, and gap-aware uncertainty intervals therefore use Draft 3 outputs.

The following analyses were not used to select the primary model and were retained from the frozen Draft 2 package rather than silently rerun under a changed protocol:

- seasonal rolling-origin evaluation;
- feature-reduction and stability analysis;
- SHAP attribution and input-group removal;
- pressure-cleaning sensitivity;
- fixed-setting algorithm checks.

Their values remain secondary evidence. The manuscript now identifies this scope explicitly. The frozen secondary analyses do not change the Draft 3 primary specification or its locked-test metrics.

## Draft 3 regenerated evidence

- 48 searches, 50 completed trials per search, 2,400 completed trials.
- 24 primary local-only fits and 24 primary local-plus-MERRA-2 fits on the historical locked test.
- Mean h1–h24 R²: 0.4125 local-only and 0.4563 full.
- Mean ΔR²: −0.0009 at h1–h6, +0.0522 at h7–h12, +0.0620 at h13–h24.
- Full-model h1 R²: 0.9488; h24 R²: 0.2044, compared with 0.2102 for local-only.
- Gap-aware 28-hour bootstrap: 1,000 paired replicates; no block crossed a missing time gap.
- Draft 3 warning means: P90 F1 0.301 full versus 0.203 local-only; P95 recall 0.099 versus 0.090.

Draft 3 uses the same historical test period as Draft 2 and is therefore a revised reanalysis, not independent external validation.
