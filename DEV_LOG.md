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
