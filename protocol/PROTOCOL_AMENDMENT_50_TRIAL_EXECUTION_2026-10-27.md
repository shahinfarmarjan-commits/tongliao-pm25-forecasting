# Draft 3 Trial-Budget Amendment

Date: 2026-10-27

The original protocol specified 100 trials per search. A validated h1 timing check showed that the available computer would require an impractical multi-hour or multi-day sequential run, and the initial parallel attempt was stopped before producing any complete Draft 3 study set. The earlier supervisor communication referred to 50 trials per search.

Draft 3 will therefore use 50 completed trials per search:

- 24 horizons x 2 specifications = 48 searches.
- 50 trials per search = 2,400 completed trials.
- 20 startup trials, followed by TPE.
- Checkpoint convergence at trials 10, 25, and 50.

All other protocol elements remain unchanged: predictor definitions, data partitions, search space, validation-RMSE objective, CatBoost seed 42, deterministic per-search Optuna seeds, early stopping, test lock, and separate output directories.

This amendment is recorded before the 50-trial run. Draft 2 remains frozen, and the incomplete 100-trial attempt is excluded from all Draft 3 results.
