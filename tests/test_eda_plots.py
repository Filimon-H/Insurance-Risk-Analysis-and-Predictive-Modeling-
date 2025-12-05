"""Basic tests for EDA plotting helpers."""

import matplotlib.pyplot as plt
import pandas as pd

from src.eda_plots import plot_histograms, plot_category_counts


def test_plot_histograms_returns_figure():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5]})

    fig = plot_histograms(df, ["x"], bins=5)

    assert isinstance(fig, plt.Figure)


def test_plot_category_counts_returns_figure():
    df = pd.DataFrame({"cat": ["A", "B", "A", "C"]})

    fig = plot_category_counts(df, "cat", top_n=2)

    assert isinstance(fig, plt.Figure)
