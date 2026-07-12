"""
Visualization module for NifftyVault.
Contains functions for plotting financial data.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_price_history(
    df,
    price_column="Adj Close",
    title="Nifty 50 Price History",
    figsize=(12, 6),
    color="#1f77b4",
    save_path=None,
    show=True,
):
    """Plot price history over time."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.index, df[price_column], label="Price", color=color)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (₹)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        return fig


def plot_returns_distribution(
    df,
    return_column="simple_return",
    title="Returns Distribution",
    figsize=(10, 6),
    color="#1f77b4",
    save_path=None,
    show=True,
):
    """Plot histogram of returns with normal overlay."""
    fig, ax = plt.subplots(figsize=figsize)
    returns = df[return_column].dropna()
    ax.hist(returns, bins=50, alpha=0.7, color=color, edgecolor="black", density=True)

    # Overlay normal distribution
    from scipy import stats

    x = np.linspace(returns.min(), returns.max(), 100)
    y = stats.norm.pdf(x, returns.mean(), returns.std())
    ax.plot(x, y, "r-", lw=2, label="Normal fit")

    ax.set_title(title)
    ax.set_xlabel("Returns")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        return fig


def plot_cumulative_returns(
    df,
    return_column="simple_return",
    title="Cumulative Returns",
    figsize=(12, 6),
    color="#1f77b4",
    save_path=None,
    show=True,
):
    """Plot cumulative returns over time."""
    # Calculate cumulative returns
    cum_returns = (1 + df[return_column]).cumprod() - 1

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(df.index, cum_returns, label="Cumulative Returns", color=color)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        return fig


def plot_rolling_metrics(
    df,
    window=30,
    return_column="simple_return",
    title="Rolling Metrics",
    figsize=(14, 8),
    save_path=None,
    show=True,
):
    """Plot rolling mean and volatility."""
    # Calculate rolling statistics
    rolling_mean = df[return_column].rolling(window=window).mean()
    rolling_std = df[return_column].rolling(window=window).std()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)

    # Rolling mean
    ax1.plot(
        df.index, rolling_mean, label=f"{window}-day Rolling Mean", color="#1f77b4"
    )
    ax1.set_title(f"{title} - Rolling Mean")
    ax1.set_ylabel("Mean Return")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Rolling volatility
    ax2.plot(
        df.index, rolling_std, label=f"{window}-day Rolling Volatility", color="#ff7f0e"
    )
    ax2.set_title(f"{title} - Rolling Volatility")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Volatility (Std Dev)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    if show:
        plt.show()
    else:
        return fig
