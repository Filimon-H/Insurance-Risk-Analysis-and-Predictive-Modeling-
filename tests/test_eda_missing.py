"""Tests for missing value EDA helpers."""

import pandas as pd
import pytest

from src.eda_missing import compute_missing_values


def test_compute_missing_values_basic():
    df = pd.DataFrame(
        {
            "A": [1, None, 3],
            "B": [None, None, 1],
        }
    )

    result = compute_missing_values(df)

    # Column B has 2/3 missing, A has 1/3 missing
    assert list(result["column"]) == ["B", "A"]
    assert list(result["missing_count"]) == [2, 1]
    assert pytest.approx(result.loc[result["column"] == "B", "missing_pct"].iloc[0], rel=1e-3) == 66.666
    assert pytest.approx(result.loc[result["column"] == "A", "missing_pct"].iloc[0], rel=1e-3) == 33.333
