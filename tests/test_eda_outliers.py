"""Tests for outlier EDA helpers."""

import pandas as pd

from src.eda_outliers import compute_high_quantiles, compute_iqr_bounds


def test_compute_high_quantiles_basic():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5]})

    result = compute_high_quantiles(df, ["x"], quantiles=[0.75, 0.9])

    assert list(result["column"]) == ["x"]
    # For [1,2,3,4,5], q75 = 4, q90 = 4.6
    assert result.loc[0, "q75"] == 4
    assert round(result.loc[0, "q90"], 1) == 4.6


def test_compute_iqr_bounds_basic():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 100]})

    lower, upper = compute_iqr_bounds(df, "x")

    # Ensure the obvious outlier 100 is above the upper bound
    assert upper < 100
