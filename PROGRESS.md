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

### [YYYY-MM-DD] To be done next

- Implement reproducible data loading and EDA helpers aligned with Task 1.
- Begin exploratory data analysis (EDA) on the insurance claims dataset.
