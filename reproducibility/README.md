# Reproducibility Notes

This release is designed for transparent review and future continuation. It is not a complete data-publication package.

## Source data

The source monitoring dataset was publicly reported by Wang et al. through Figshare. It is not copied into this repository. NASA MERRA-2 source data are also not copied here. Reproduction requires obtaining both sources independently and confirming their current access terms.

The public source does not verify all station metadata, including exact station identity, coordinates, elevation, logger timezone, and timestamp semantics. The manuscript therefore treats the extraction domain and timing convention as study assumptions and reports them as limitations.

## Model structure

- Local-only specification: 149 predictors.
- Local plus MERRA-2 specification: 222 predictors.
- Forecast horizons: 24 direct models for each specification.
- Primary learner: CatBoost.
- Primary locked-test comparison: identical target rows for the two specifications at each horizon.
- Data split: chronological target-time training, validation, and locked test.

The two reference scripts in `source/` now read the project location from the `TONGLIAO_PROJECT_ROOT` environment variable. They still require the omitted source inputs and full pipeline outputs, so they are included as documented reference code rather than as a turnkey rerun.

## Included results

The `results/` folder contains selected tables from the locked-test evaluation and the gap-aware uncertainty audit. The audit used archived predictions and did not refit or retune the primary models.

The gap-aware audit sampled paired target blocks only within continuous calendar-time runs. It used 1,000 replicates at 28, 48, 72, and 168 hour block lengths. The point estimates remained the same as the archived evaluation; the intervals widened with longer blocks.

## Reuse

The included PDFs and figures should be treated as research outputs with their manuscript context. No open-source software license or data redistribution license is assigned by this repository unless a later release adds one. Please cite the manuscript and the original data providers when using these materials.

## Excluded materials

Raw monitoring files, MERRA-2 downloads, intermediate model artifacts, private correspondence, credentials, temporary render files, unfinished drafts, and exact location details are excluded. The `.gitignore` file provides additional protection against accidentally adding common raw-data and local-environment files.
