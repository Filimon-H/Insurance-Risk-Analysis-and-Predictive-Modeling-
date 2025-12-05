"""Tests for ZipCode-based EDA helpers."""

import pandas as pd

from src.eda_zipcode import compute_monthly_totals_by_postal, summarise_postal_averages


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PostalCode": [1000, 1000, 2000, 2000],
            "TransactionMonth": [
                "2015-01-01",
                "2015-02-01",
                "2015-01-01",
                "2015-02-01",
            ],
            "TotalPremium": [100.0, 200.0, 300.0, 400.0],
            "TotalClaims": [50.0, 0.0, 150.0, 200.0],
        }
    )


def test_compute_monthly_totals_by_postal_basic():
    df = _sample_df()

    grouped = compute_monthly_totals_by_postal(df)

    # Expect 4 rows (2 postcodes x 2 months)
    assert len(grouped) == 4
    assert set(grouped.columns) == {
        "PostalCode",
        "month",
        "total_premium",
        "total_claims",
        "loss_ratio",
    }


def test_summarise_postal_averages_basic():
    df = _sample_df()
    grouped = compute_monthly_totals_by_postal(df)

    summary = summarise_postal_averages(grouped)

    # Expect 2 rows, one per PostalCode
    assert set(summary["PostalCode"]) == {1000, 2000}
    assert "avg_monthly_premium" in summary.columns
    assert "avg_monthly_claims" in summary.columns
    assert "avg_monthly_loss_ratio" in summary.columns
