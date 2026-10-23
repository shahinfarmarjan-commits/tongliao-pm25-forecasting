# PM2.5 Forecasting in Open-Pit Mining

This repository records the public research materials for:

**PM2.5 Forecasting in Open-Pit Mining: Horizon-Dependent Predictive Value of Local Monitoring and Regional Atmospheric Information**

The study evaluates hourly mine-area PM2.5 forecasts from 1 to 24 hours ahead. It compares a local-only CatBoost model with a matched model that also uses regional NASA MERRA-2 atmospheric reanalysis information.

## Main finding

Recent local monitoring was most useful for immediate forecasts. MERRA-2 provided little average benefit at h1-h6 and clearer average predictive value at longer horizons:

- h1-h6: Delta R2 = -0.0011
- h7-h12: Delta R2 = +0.0409
- h13-h24: Delta R2 = +0.0625
- Full h1-h24 model: R2 = 0.4473
- Local-only h1-h24 model: R2 = 0.4060

These are predictive associations. SHAP values describe model attribution and do not establish physical causation.

## Repository contents

- `paper/`: current Draft 2 Version 3 manuscript and supplementary PDF files.
- `results/`: selected locked-test metrics and the gap-aware uncertainty sensitivity.
- `figures/`: selected publication and presentation figures.
- `poster/`: a preview of the RAIS2026 poster.
- `history/`: a condensed record of the project decisions and conversation milestones.
- `reproducibility/`: analysis scope, provenance, and code notes.

## Important evidence boundaries

- The 222-predictor full model is the primary locked-test specification.
- The 149-predictor local-only model is the matched comparison.
- The 59-predictor candidate is post-hoc and validation-only.
- MERRA-2 is regional atmospheric reanalysis information, not a mine-level sensor or a simple synonym for satellite data.
- The study estimates historical predictive value. MERRA-2 delivery latency was not modeled, so real-time operational performance was not established.
- Seasonal results are secondary rolling-origin analyses from the available record.
- Rare-event warning use requires timely data and new mine-period validation.

## Data and privacy

Raw monitoring data, credentials, private correspondence, unfinished drafts, temporary files, and exact location details are intentionally excluded from this public repository. The source monitoring dataset is publicly described by Wang et al.; users who need to reproduce the analysis should obtain the source data independently and follow its terms.

The repository is a public research record, not a complete executable rerun package. See `reproducibility/README.md` for the current limitations.

## Manuscript status

The current manuscript package still contains author-dependent declarations that must be finalized before journal submission, including AI use, funding, conflicts of interest, ethics/data availability, and CRediT roles.
