"""
Tests for the visualization module.
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt

from nifftyvault.visualization import (
    plot_cumulative_returns,
    plot_price_history,
    plot_returns_distribution,
    plot_rolling_metrics,
)


def test_plot_price_returns(sample_price_data):
    fig = plot_price_history(sample_price_data, show=False)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)


def test_plot_returns_distribution(sample_returns_data):
    fig = plot_returns_distribution(sample_returns_data, show=False)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)


def test_plot_cumulative_returns(sample_returns_data):
    fig = plot_cumulative_returns(sample_returns_data, show=False)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)


def test_plot_rolling_metrics(sample_returns_data):
    fig = plot_rolling_metrics(sample_returns_data, window=5, show=False)
    assert isinstance(fig, matplotlib.figure.Figure)
    plt.close(fig)
