"""EDA summary utilities for insurance risk analysis.

This module contains small helper functions for computing
portfolio-level metrics such as loss ratios.
"""

from __future__ import annotations

import pandas as pd


def compute_loss_ratio_overall(df: pd.DataFrame) -> float:
    """Compute the overall loss ratio for the portfolio.

    Loss ratio is defined as TotalClaims / TotalPremium.
    Returns 0.0 if the total premium is zero to avoid division by zero.
    """

    total_premium = df["TotalPremium"].sum()
    total_claims = df["TotalClaims"].sum()

    if total_premium == 0:
        return 0.0

    return float(total_claims / total_premium)


def compute_loss_ratio_by_group(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    """Compute loss ratio aggregated by one or more grouping columns.

    Parameters
    ----------
    df:
        Input DataFrame containing at least TotalPremium and TotalClaims.
    group_cols:
        List of column names to group by, e.g. ["Province"],
        ["Province", "VehicleType"], etc.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the grouping columns plus:
        - total_premium
        - total_claims
        - loss_ratio
    """

    grouped = (
        df.groupby(group_cols, dropna=False)[["TotalPremium", "TotalClaims"]]
        .sum()
        .rename(columns={
            "TotalPremium": "total_premium",
            "TotalClaims": "total_claims",
        })
    )

    grouped["loss_ratio"] = grouped.apply(
        lambda row: 0.0 if row["total_premium"] == 0 else row["total_claims"] / row["total_premium"],
        axis=1,
    )

    return grouped.reset_index()
