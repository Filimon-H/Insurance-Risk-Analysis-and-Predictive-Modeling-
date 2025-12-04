"""EDA helpers for time trends (e.g. monthly loss ratios)."""

from __future__ import annotations

import pandas as pd


def prepare_monthly_loss_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly loss ratio over TransactionMonth.

    Assumes `TransactionMonth` is a string or datetime-like column.
    Returns a DataFrame with:
    - month (period or datetime)
    - total_premium
    - total_claims
    - loss_ratio
    """

    if "TransactionMonth" not in df.columns:
        raise KeyError("TransactionMonth column not found in DataFrame")

    df_local = df.copy()
    df_local["TransactionMonth"] = pd.to_datetime(df_local["TransactionMonth"])
    df_local["month"] = df_local["TransactionMonth"].dt.to_period("M").dt.to_timestamp()

    grouped = (
        df_local.groupby("month")[["TotalPremium", "TotalClaims"]]
        .sum()
        .rename(columns={"TotalPremium": "total_premium", "TotalClaims": "total_claims"})
    )

    grouped["loss_ratio"] = grouped.apply(
        lambda row: 0.0 if row["total_premium"] == 0 else row["total_claims"] / row["total_premium"],
        axis=1,
    )

    return grouped.reset_index()
