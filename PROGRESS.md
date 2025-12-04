# Project Progress Log

## Overview

This repository contains an insurance risk analysis and predictive modeling project
for car insurance in South Africa. The goal is to analyse historical insurance
claims, perform statistical testing, and build predictive models for risk-based pricing.

## Milestones

### [YYYY-MM-DD] Initial setup

- Basic repository structure created (.github, src, notebooks, tests, scripts).
- Logging and documentation workflow defined (`PROGRESS.md`, `DEV_LOG.md`).

### [YYYY-MM-DD] Configuration and testing setup

- Implemented `src/config.py` with a `Config` class and `get_config()` helper.
- Added `.env.example` and updated `.gitignore` to exclude `.env` and `logs/`.
- Created `tests/test_config.py` with initial pytest unit tests.
- Configured `.github/workflows/unittests.yml` to run pytest in CI on pushes and pull requests.

### [YYYY-MM-DD] Task 1 – initial EDA setup

- Implemented `src/data_loader.py` and `tests/test_data_loader.py` for robust loading of `data/raw/MachineLearningRating_v3.txt`.
- Added `src/eda_summary.py` and `tests/test_eda_summary.py` to compute and validate overall and grouped loss ratios.
- Created `notebooks/01_task1_eda_overview.ipynb` to inspect the dataset, compute loss ratios, and prepare for deeper EDA.

### [YYYY-MM-DD] To be done next

- Extend EDA to include missing value analysis, distributions, outlier detection, and time trends.
- Produce at least three high-quality visualisations that highlight key risk and profitability insights.
