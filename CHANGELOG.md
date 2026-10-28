# Changelog

## Draft 3, 2026-10-28

- Increased the primary Optuna budget from 10 to 50 completed trials per search.
- Completed 48 validation-only searches and 2,400 trials.
- Used 20 startup trials, adaptive TPE, deterministic per-search sampler seeds, and CatBoost seed 42.
- Regenerated primary locked-test predictions after all searches completed.
- Added convergence checkpoints at trials 10, 25, and 50.
- Added gap-aware paired 28-hour bootstrap summaries with 1,000 replicates.
- Updated the manuscript, supplement, primary performance figure, and Draft 2 comparison.
- Explicitly reconciled secondary analyses that were retained from the frozen Draft 2 package.

## Draft 2 archive

Draft 2 remains frozen in the private project archive and is not overwritten by this release.
