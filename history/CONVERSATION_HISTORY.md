# Conversation and Project History

This is a condensed, public-safe record of the work discussed from the first manuscript and figure decisions through the current repository release. Private email text, personal contact details, raw data, and exact location information are omitted.

## Manuscript and figure development

1. The project began with Draft 1 figures and Draft 2 text. The selected working version preserved the edited Draft 2 text while retaining the original figures unless a replacement was explicitly requested.
2. A separate Draft 2 Version 2 package was created for figure work so that the earlier manuscript package remained safe.
3. Study-design and forecasting figures were reviewed for scientific accuracy, caption fit, readability, and placement in the main paper or supplement.
4. The manuscript was checked for grammar, terminology, numerical consistency, scientific boundaries, cross-references, and figure quality.
5. The paper was revised to keep SHAP interpretation attribution-based rather than causal. The 222-predictor model remained the sole primary locked-test result, while the 59-predictor analysis remained post-hoc and validation-only.
6. Technical terminology was simplified selectively. Methods terminology such as SHAP, CatBoost, MERRA-2, locked test, post-hoc, and validation-only was retained where precision required it.
7. The title was revised to: `PM2.5 Forecasting in Open-Pit Mining: Horizon-Dependent Predictive Value of Local Monitoring and Regional Atmospheric Information`.
8. Seasonal results were framed as a strong secondary finding: winter had the highest PM2.5 burden, while autumn showed the largest average MERRA-2 gain. Possible physical explanations were kept explicitly hypothetical because haulage, blasting, watering, road-moisture, and production-rate data were unavailable.
9. Exact mine coordinates, grid-cell coordinates, exact area weights, and the location map were removed from the ready manuscript package because the public source does not provide verified station provenance.
10. Draft 2 Version 3 was assembled as the ready manuscript package. Draft 1 was preserved as a historical comparison and was not modified.

## Presentations and poster

11. A thesis seminar presentation was prepared with speaker notes on every slide. Its central story is the change in useful information across forecast horizons.
12. A separate RAIS2026 poster was developed for a general AI and engineering audience. The visual story is: local recent history supports immediate forecasts, while regional atmospheric information becomes more useful for longer planning horizons.
13. Poster figures were selected to show horizon-dependent MERRA-2 value, the SHAP attribution shift, and the seasonal contrast. Dense technical figures and exact location maps were kept out of the public-facing poster.

## Reproducibility and scientific review

14. An EDA evidence pack and new-chat handoff were prepared so later analysis can use the same verified counts, model definitions, and evidence hierarchy.
15. The Optuna audit confirmed 48 searches, 10 completed trials per search, and 480 completed trials total. The searches remained in the startup phase; adaptive TPE did not begin. This limitation is disclosed rather than described as global hyperparameter optimization.
16. A referee-style audit compared Draft 1 and Draft 2. Draft 2 was judged clearer and better organized, while Draft 1 retained stronger provenance and seasonal uncertainty detail. The recommended journal base is a hybrid of the two.
17. The audit identified inconsistent wording about MERRA-2 delivery availability and a forecast-origin boundary that required clarification. Excluding the affected early boundary rows did not change the central results.
18. The audit also identified that the original main-test circular row bootstrap could cross missing calendar-hour gaps. A gap-aware paired sensitivity was run with 28, 48, 72, and 168 hour blocks. Point estimates remained stable, while longer blocks produced wider intervals.

## Current release

19. This public repository was created as a sanitized research archive. It contains selected final paper materials, selected results, core figures, the poster preview, and this project history. Raw monitoring data, private correspondence, temporary files, credentials, unfinished working folders, and exact location details are excluded.
