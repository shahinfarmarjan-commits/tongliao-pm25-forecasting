# Tongliao PM2.5 Forecasting

Draft 3 release materials for:

**PM2.5 Forecasting in Open-Pit Mining: Horizon-Dependent Predictive Value of Local Monitoring and Regional Atmospheric Information**

This release contains the sanitized paper package and selected reproducibility artifacts for the 50-trial Draft 3 reanalysis. The study compares local-only and local-plus-MERRA-2 CatBoost models for hourly PM2.5 forecasting from 1 to 24 hours ahead.

## Draft 3 primary analysis

- 24 forecast horizons × 2 predictor specifications = 48 searches.
- 50 completed validation-only Optuna trials per search = 2,400 completed trials.
- 20 startup trials followed by adaptive TPE.
- Chronological training, validation, and one-time historical locked-test evaluation.
- Mean locked-test R²: 0.4125 for local-only and 0.4563 for local plus MERRA-2.
- Mean ΔR²: −0.0009 at h1–h6, +0.0522 at h7–h12, and +0.0620 at h13–h24.
- Full-model h1 R²: 0.9488; h24 R²: 0.2044, compared with 0.2102 for local-only.

Draft 3 uses the same historical test period as Draft 2. It is a revised reanalysis, not independent external validation. Seasonal, SHAP, ablation, and feature-reduction analyses are identified in the manuscript as retained secondary evidence when their original protocol was not rerun.

## Contents

- `paper/`: Draft 3 manuscript and supplementary material in DOCX and PDF formats.
- `results/`: selected metrics, convergence checkpoints, horizon-band comparisons, and gap-aware uncertainty summaries.
- `protocol/`: dated trial-budget amendment and validation notes.
- `figures/`: updated primary performance figure.
- `history/`: Draft 2 versus Draft 3 comparison and secondary-analysis reconciliation.

Raw monitoring data, MERRA-2 files, exact coordinates, private correspondence, and unfinished runs are not included.

## Data and code

The monitoring dataset was published by Wang et al. through Figshare: https://doi.org/10.6084/m9.figshare.21308433.v2. MERRA-2 data are available from NASA GES DISC: https://doi.org/10.5067/KLICLTZ8EM9D. The full local working archive is not part of this public release.
