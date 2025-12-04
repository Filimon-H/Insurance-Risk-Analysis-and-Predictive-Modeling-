"""Basic tests for EDA plotting helpers."""

import matplotlib.pyplot as plt
import pandas as pd

from src.eda_plots import plot_histograms


def test_plot_histograms_returns_figure():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5]})

    fig = plot_histograms(df, ["x"], bins=5)

    assert isinstance(fig, plt.Figure)
