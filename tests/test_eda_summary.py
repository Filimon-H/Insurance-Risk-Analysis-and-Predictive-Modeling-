"""Tests for EDA summary helper functions.

We use a small in-memory DataFrame to validate loss ratio
calculations overall and by groups.
"""

import pandas as pd

from src.eda_summary import (
    compute_loss_ratio_overall,
    compute_loss_ratio_by_group,
    summarise_numerics,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Province": ["A", "A", "B"],
            "TotalPremium": [100.0, 300.0, 600.0],
            "TotalClaims": [50.0, 0.0, 300.0],
        }
    )


def test_compute_loss_ratio_overall_basic():
    df = _sample_df()

    lr = compute_loss_ratio_overall(df)

    # total_premium = 100 + 300 + 600 = 1000
    # total_claims  = 50 +   0 + 300 = 350 -> 0.35
    assert lr == 0.35


def test_compute_loss_ratio_overall_zero_premium_returns_zero():
    df = pd.DataFrame({"TotalPremium": [0.0, 0.0], "TotalClaims": [10.0, 0.0]})

    lr = compute_loss_ratio_overall(df)

    assert lr == 0.0


def test_compute_loss_ratio_by_group_single_column():
    df = _sample_df()

    result = compute_loss_ratio_by_group(df, ["Province"])

    # For Province A: premium = 400, claims = 50 -> 0.125
    # For Province B: premium = 600, claims = 300 -> 0.5
    result_sorted = result.sort_values("Province").reset_index(drop=True)

    assert list(result_sorted["Province"]) == ["A", "B"]
    assert list(result_sorted["total_premium"]) == [400.0, 600.0]
    assert list(result_sorted["total_claims"]) == [50.0, 300.0]
    assert list(result_sorted["loss_ratio"]) == [0.125, 0.5]


def test_summarise_numerics_returns_describe_like_table():
    df = _sample_df()

    summary = summarise_numerics(df, ["TotalPremium", "TotalClaims"])

    # Index should be the column names we passed
    assert set(summary.index) == {"TotalPremium", "TotalClaims"}
    # Expect standard describe statistics columns
    for col in ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]:
        assert col in summary.columns
