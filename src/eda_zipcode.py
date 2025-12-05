"""EDA helpers for ZipCode (PostalCode) based analysis."""

from __future__ import annotations

import pandas as pd


def compute_monthly_totals_by_postal(df: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly totals of premium and claims by PostalCode.

    Returns columns:
    - PostalCode
    - month
    - total_premium
    - total_claims
    - loss_ratio
    """

    df_local = df.copy()
    df_local["TransactionMonth"] = pd.to_datetime(df_local["TransactionMonth"])
    df_local["month"] = df_local["TransactionMonth"].dt.to_period("M").dt.to_timestamp()

    grouped = (
        df_local.groupby(["PostalCode", "month"])[["TotalPremium", "TotalClaims"]]
        .sum()
        .rename(columns={"TotalPremium": "total_premium", "TotalClaims": "total_claims"})
        .reset_index()
    )

    grouped["loss_ratio"] = grouped.apply(
        lambda row: 0.0 if row["total_premium"] == 0 else row["total_claims"] / row["total_premium"],
        axis=1,
    )

    return grouped


def summarise_postal_averages(grouped: pd.DataFrame) -> pd.DataFrame:
    """Summarise average monthly premium and claims per PostalCode.

    Input is the output of compute_monthly_totals_by_postal.
    Returns columns:
    - PostalCode
    - avg_monthly_premium
    - avg_monthly_claims
    - avg_monthly_loss_ratio
    """

    summary = (
        grouped.groupby("PostalCode")[["total_premium", "total_claims", "loss_ratio"]]
        .mean()
        .rename(
            columns={
                "total_premium": "avg_monthly_premium",
                "total_claims": "avg_monthly_claims",
                "loss_ratio": "avg_monthly_loss_ratio",
            }
        )
        .reset_index()
    )




    return summary
