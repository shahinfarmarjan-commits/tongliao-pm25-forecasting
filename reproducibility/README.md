# Reproducibility Notes

This public release is a sanitized research-output package, not a turnkey rerun. Raw monitoring data, MERRA-2 files, exact coordinates, and full intermediate artifacts are intentionally excluded.

## Draft 3 primary analysis

- 149-predictor local-only and 222-predictor local-plus-MERRA-2 CatBoost specifications.
- Twenty-four direct forecast horizons for each specification.
- Chronological target-time training, validation, and historical locked test.
- 48 validation-only Optuna searches, 50 completed trials per search, 2,400 total trials.
- 20 startup trials followed by adaptive TPE and deterministic per-search sampler seeds.
- Test scoring began only after all tuning searches completed.

Selected metrics, convergence checkpoints, horizon-band comparisons, warning means, and gap-aware bootstrap intervals are in `results/`. The manuscript and supplement define the feature contract and preprocessing rules.

Reproduction requires obtaining the source monitoring dataset from Figshare and NASA MERRA-2 independently, confirming access terms, and rebuilding the omitted local pipeline. The public source does not verify all station metadata, so the manuscript reports provenance and timing limitations explicitly.
