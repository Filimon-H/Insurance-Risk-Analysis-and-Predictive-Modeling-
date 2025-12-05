"""Plotting helpers for EDA."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd


def plot_histograms(
    df: pd.DataFrame,
    columns: Iterable[str],
    bins: int = 50,
    log_scale: bool = False,
) -> plt.Figure:
    """Plot simple histograms for the given numeric columns.

    Returns the created matplotlib Figure so callers can further
    customise or save it.
    """

    cols = list(columns)
    n = len(cols)
    if n == 0:
        raise ValueError("No columns provided for plotting")

    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, col in zip(axes, cols):
        series = df[col].dropna()
        ax.hist(series, bins=bins)
        ax.set_title(col)
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        if log_scale:
            ax.set_yscale("log")

    fig.tight_layout()
    return fig


def plot_category_counts(
    df: pd.DataFrame,
    column: str,
    top_n: int | None = None,
) -> plt.Figure:
    """Plot a bar chart of category counts for a given column.

    Parameters
    ----------
    df:
        Input DataFrame.
    column:
        Name of the categorical column to count.
    top_n:
        If provided, only the top_n most frequent categories are shown.
    """

    counts = df[column].value_counts(dropna=False)
    if top_n is not None:
        counts = counts.head(top_n)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index.astype(str), counts.values)
    ax.set_title(f"Count by {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig
