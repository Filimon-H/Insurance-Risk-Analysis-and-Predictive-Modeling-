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
