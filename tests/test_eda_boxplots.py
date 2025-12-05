"""Tests for boxplot EDA helpers."""

import matplotlib.pyplot as plt
import pandas as pd

from src.eda_boxplots import plot_boxplot


def test_plot_boxplot_returns_figure():
    df = pd.DataFrame({"x": [1, 2, 3, 100]})

    fig = plot_boxplot(df, "x", log_scale=True)

    assert isinstance(fig, plt.Figure)
