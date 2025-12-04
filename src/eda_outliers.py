"""EDA helpers for outlier analysis."""

from __future__ import annotations

import pandas as pd


def compute_high_quantiles(
    df: pd.DataFrame,
    columns: list[str],
    quantiles: list[float] | None = None,
) -> pd.DataFrame:
    """Compute high quantiles for selected numeric columns.

    Parameters
    ----------
    df:
        Input DataFrame.
    columns:
        Numeric columns to analyse.
    quantiles:
        List of quantiles between 0 and 1. Defaults to [0.75, 0.9, 0.95, 0.99].
    """

    if quantiles is None:
        quantiles = [0.75, 0.9, 0.95, 0.99]

    q_df = df[columns].quantile(quantiles).T
    q_df.columns = [f"q{int(q * 100)}" for q in quantiles]
    q_df = q_df.reset_index().rename(columns={"index": "column"})

    return q_df


def compute_iqr_bounds(df: pd.DataFrame, column: str) -> tuple[float, float]:
    """Compute IQR-based lower and upper bounds for a single column.

    Returns (lower_bound, upper_bound) where:
    - lower_bound = Q1 - 1.5 * IQR
    - upper_bound = Q3 + 1.5 * IQR
    """

    series = df[column].dropna()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = float(q1 - 1.5 * iqr)
    upper = float(q3 + 1.5 * iqr)
    return lower, upper
