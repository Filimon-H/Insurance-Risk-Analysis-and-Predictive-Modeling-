# Development Log

## [YYYY-MM-DD] Step 1 – Project logging setup

**Context**

- Establish a clear, auditable record of progress and decisions.
- Separate high-level progress (`PROGRESS.md`) from detailed development notes (`DEV_LOG.md`).

**Changes in this step**

- Added `PROGRESS.md` to track milestones and overall project status.
- Added `DEV_LOG.md` to keep a detailed, chronological record of development steps.

**Intended commit message**

- `chore: add project progress and development log files`

## [YYYY-MM-DD] Step 2 – Configuration module, tests, and CI

**Context**

- Provide a single source of truth for important paths and flags.
- Prepare the codebase for future modules (EDA, DVC, modeling) with a clean configuration layer and automated testing.

**Changes in this step**

- Added `src/config.py` with a `Config` dataclass and `get_config()` helper that reads environment variables (optionally from `.env`) and falls back to sensible defaults.
- Introduced `.env.example` and updated `.gitignore` to ignore `.env` and the `logs/` directory.
- Added `tests/test_config.py` with basic pytest unit tests for the configuration behaviour.
- Configured GitHub Actions workflow in `.github/workflows/unittests.yml` to run `pytest` on pushes and pull requests.

**Intended commit message**

- `feat: add configuration module with pytest tests and CI workflow`

## [YYYY-MM-DD] Step 3 – Task 1 data loader and initial EDA helpers

**Context**

- Begin Task 1 by creating a reusable data loading layer and basic EDA metrics.
- Ensure all logic is modular and covered by unit tests before using it in notebooks.

**Changes in this step**

- Added `src/data_loader.py` with a `DataLoader` class that loads the `MachineLearningRating_v3.txt` dataset from `data/raw` using the configured `data_dir` and the correct pipe (`|`) separator.
- Created `tests/test_data_loader.py` to validate the loader behaviour, including respecting `Config.data_dir`, handling missing files, and correctly reading a small sample file.
- Implemented `src/eda_summary.py` with `compute_loss_ratio_overall` and `compute_loss_ratio_by_group` helper functions for portfolio and grouped loss ratios.
- Added `tests/test_eda_summary.py` to verify the correctness of the loss ratio computations on a small in-memory DataFrame.
- Created `notebooks/01_task1_eda_overview.ipynb` to load the dataset, inspect its structure, and compute overall and grouped loss ratios using the helper functions.

**Intended commit messages**

- `feat: add data loader for MachineLearningRating_v3 dataset`
- `feat: add loss ratio EDA helpers with unit tests`
- `feat: add Task 1 EDA overview notebook`

## [YYYY-MM-DD] Step 4 – Missing values EDA helper

**Context**

- Extend Task 1 EDA with a clear overview of missing data patterns.
- Keep the logic reusable and covered by tests, then surface results in the notebook.

**Changes in this step**

- Added `src/eda_missing.py` with `compute_missing_values` to compute per-column missing counts and percentages, sorted by highest missing percentage.
- Created `tests/test_eda_missing.py` to validate the helper on a small DataFrame, checking ordering, counts, and percentages using `pytest.approx`.
- Updated `notebooks/01_task1_eda_overview.ipynb` to import `compute_missing_values` and display a table of missing-value statistics.

**Intended commit message**

- `feat: add missing values EDA helper and notebook cell`

## [YYYY-MM-DD] Step 5 – Distributions, outliers, and time trends for Task 1

**Context**

- Round out Task 1 EDA by visualising key distributions, identifying outliers, and examining monthly loss ratio trends.
- Add simple visual summaries for gender and provincial risk differences to support later hypothesis testing.

**Changes in this step**

- Added `src/eda_plots.py` and `tests/test_eda_plots.py` with a `plot_histograms` helper for basic numeric distributions.
- Implemented `src/eda_outliers.py` and `tests/test_eda_outliers.py` to compute high quantiles and IQR bounds for outlier analysis.
- Implemented `src/eda_trends.py` and `tests/test_eda_trends.py` to compute monthly loss ratios from `TransactionMonth`.
- Extended `notebooks/01_task1_eda_overview.ipynb` with:
  - Histogram plots for `TotalPremium` and `TotalClaims`.
  - High-quantile summary for `TotalPremium` and `TotalClaims`.
  - Monthly loss ratio table and line chart over time.
  - Additional cells for loss ratio by `Gender` and a bar plot of loss ratio by `Province`.

**Intended commit messages**

- `feat: add histogram EDA helper and notebook plots`
- `feat: add outlier EDA helpers and quantile summary cell`
- `feat: add monthly loss ratio trend helper and plots`

## [YYYY-MM-DD] Step 6 – Finalise Task 1 EDA checklist

**Context**

- Complete all remaining items from the Task 1 checklist, ensuring both code and notebook cover: descriptive statistics, categorical distributions, ZipCode analysis, geographic comparisons, and boxplot-based outlier detection.

**Changes in this step**

- Extended `src/eda_summary.py` with `summarise_numerics` and tests in `tests/test_eda_summary.py` to provide descriptive statistics for key numeric variables.
- Enhanced `src/eda_plots.py` and `tests/test_eda_plots.py` with `plot_category_counts` for categorical distributions (e.g. counts by `Province` and `VehicleType`).
- Added `src/eda_zipcode.py` and `tests/test_eda_zipcode.py` to compute monthly totals and averages of premiums/claims by `PostalCode` and to summarise ZipCode-level behaviour.
- Introduced `src/eda_boxplots.py` and `tests/test_eda_boxplots.py` to visualise outliers via boxplots for `TotalPremium` and `TotalClaims`.
- Updated `notebooks/01_task1_eda_overview.ipynb` with:
  - Descriptive stats tables for key numeric variables.
  - Count bar charts for `Province` and `VehicleType`.
  - ZipCode-level top-20 table and a scatter plot of average monthly premium vs claims.
  - Boxplots for `TotalPremium` and `TotalClaims`, plus interpretation markdown after each major analysis.

**Intended commit messages**

- `feat: add numeric descriptive statistics helper and notebook cell`
- `feat: add categorical count plots for Province and VehicleType`
- `feat: add ZipCode-based monthly premium/claims analysis and scatter plot`
- `feat: add boxplot helpers and outlier visualisation cells`
