"""EDA helpers for missing value analysis."""

from __future__ import annotations

import pandas as pd


def compute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Compute missing value counts and percentages for each column.

    Returns a DataFrame with columns:
    - column
    - missing_count
    - missing_pct (0–100)
    """

    total_rows = len(df)
    if total_rows == 0:
        return pd.DataFrame(columns=["column", "missing_count", "missing_pct"])

    missing_count = df.isna().sum()
    missing_pct = (missing_count / total_rows * 100).astype(float)

    result = (
        pd.DataFrame(
            {
                "column": missing_count.index,
                "missing_count": missing_count.values,
                "missing_pct": missing_pct.values,
            }
        )
        .sort_values("missing_pct", ascending=False)
        .reset_index(drop=True)
    )

    return result
