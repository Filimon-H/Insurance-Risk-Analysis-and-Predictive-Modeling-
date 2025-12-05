"""Boxplot helpers for outlier visualisation."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_boxplot(df: pd.DataFrame, column: str, log_scale: bool = False) -> plt.Figure:
    """Create a boxplot for a single numeric column.

    Parameters
    ----------
    df:
        Input DataFrame.
    column:
        Name of the numeric column to plot.
    log_scale:
        If True, use log scale on the y-axis to better visualise tails.
    """

    series = df[column].dropna()

    fig, ax = plt.subplots(figsize=(4, 6))
    ax.boxplot(series, vert=True)
    ax.set_title(f"Boxplot of {column}")
    ax.set_ylabel(column)
    if log_scale:
        ax.set_yscale("log")
    fig.tight_layout()
    return fig
