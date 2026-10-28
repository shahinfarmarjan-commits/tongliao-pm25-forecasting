# Conversation and Project History

This is a condensed public-safe record of the project and Draft 3 release. Private email text, personal contact details, raw data, and exact location information are omitted.

## Manuscript and figure development

1. Draft 2 Version 3 was frozen as the comparison baseline.
2. The manuscript retained the 222-predictor model as the predefined locked-test specification and the 59-predictor model as post-hoc validation-only evidence.
3. The title was revised to: `PM2.5 Forecasting in Open-Pit Mining: Horizon-Dependent Predictive Value of Local Monitoring and Regional Atmospheric Information`.
4. Seasonal results were framed as a secondary finding: winter had the highest PM2.5 burden, while autumn showed the largest average MERRA-2 gain.
5. Exact mine coordinates, grid-cell coordinates, exact area weights, and the location map were excluded from the public-ready paper package.

## Draft 3 reanalysis

6. The primary budget was amended before execution from 100 to 50 completed trials per search, consistent with the supervisor communication and the available compute budget.
7. The final run completed 48 searches, 50 trials per search, and 2,400 completed validation-only trials.
8. Each search used 20 startup trials followed by adaptive TPE, deterministic per-search sampler seeds, and CatBoost seed 42.
9. The historical locked test was opened only after all tuning searches completed.
10. Draft 3 mean locked-test R2 was 0.4125 for local-only and 0.4563 for local plus MERRA-2.
11. Mean delta R2 was -0.0009 at h1-h6, +0.0522 at h7-h12, and +0.0620 at h13-h24.
12. A paired gap-aware 28-hour bootstrap used 1,000 replicates without crossing missing time gaps.

## Scope

Draft 3 uses the same historical test period as Draft 2 and is therefore a revised reanalysis, not independent external validation. Secondary analyses are labeled according to whether they were rerun under the Draft 3 protocol or retained from the frozen Draft 2 package.
