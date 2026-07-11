"""
Analysis module for NifftyVault.
Contains functions for financial metrics calculation.
"""

import numpy as np
import pandas as pd


def load_data(filename="nifty_50_data.csv"):
    """Load the CSV data and drop NaN rows."""
    df = pd.read_csv(filename, index_col=0, parse_dates=True)
    df = df.dropna()  # Remove first row with NaN return
    return df


def annualized_return(df, column="simple_return"):
    """Compute annualized return from daily returns."""
    daily_mean = df[column].mean()
    trading_days = 252  # approximate
    annual_ret = (1 + daily_mean) ** trading_days - 1
    return annual_ret


def annualized_volatility(df, column="simple_return"):
    """Compute annualized volatility from daily returns."""
    daily_std = df[column].std()
    trading_days = 252
    annual_vol = daily_std * np.sqrt(trading_days)
    return annual_vol


def sharpe_ratio(df, risk_free_rate=0.0, column="simple_return"):
    """Compute annualized Sharpe ratio."""
    ann_ret = annualized_return(df, column)
    if not isinstance(ann_ret, (int, float, np.number)):
        ann_ret = ann_ret.iloc[0] if hasattr(ann_ret, "iloc") else float(ann_ret)
    ann_vol = annualized_volatility(df, column)
    if np.isclose(ann_vol, 0.0):
        return np.inf
    sharpe = (ann_ret - risk_free_rate) / ann_vol
    return sharpe


def sortino_ratio(df, risk_free_rate=0.0, column="simple_return"):
    """Compute annualized Sortino ratio (downside deviation)."""
    daily_returns = df[column]
    excess_returns = daily_returns - risk_free_rate / 252  # daily risk-free
    downside_returns = excess_returns[excess_returns < 0]
    if len(downside_returns) == 0:
        return np.inf
    downside_std = downside_returns.std()
    annualized_downside = downside_std * np.sqrt(252)
    annual_excess = (daily_returns.mean() * 252) - risk_free_rate
    if annualized_downside == 0:
        return np.inf
    return annual_excess / annualized_downside


def var_parametric(df, confidence=0.95, column="simple_return"):
    """Compute parametric Value at Risk (VaR) at given confidence level."""
    # Assuming normal distribution
    mean = df[column].mean()
    std = df[column].std()
    from scipy import stats

    cutoff = stats.norm.ppf(1 - confidence, mean, std)
    return cutoff  # negative value, represents loss


def max_drawdown(df, price_column="Adj Close"):
    """Compute maximum drawdown from price drawdown from price series."""
    # Compute cumulative max
    cumulative_max = df[price_column].cummax()
    # Drawdown = (current - cumulative_max) / cumulative_max
    drawdown = (df[price_column] - cumulative_max) / cumulative_max
    max_dd = drawdown.min()  # most negative value
    return max_dd


def calculate_all_metrics(
    df, price_column="Adj Close", return_column="simple_return", risk_free_rate=0.0
):
    """Calculate all common metrics and return as dictionary."""
    # Ensure return column exists; if not, compute simple return from price column
    if return_column not in df.columns:
        # Compute simple return (pct_change) and fill first NaN with 0
        returns = df[price_column].pct_change().fillna(0)
        # Use a temporary DataFrame to avoid modifying original
        df_temp = df.copy()
        df_temp[return_column] = returns
        data_for_calc = df_temp
    else:
        data_for_calc = df

    metrics = {
        "annualized_return": annualized_return(data_for_calc, return_column),
        "annualized_volatility": annualized_volatility(data_for_calc, return_column),
        "sharpe_ratio": sharpe_ratio(data_for_calc, risk_free_rate, return_column),
        "sortino_ratio": sortino_ratio(data_for_calc, risk_free_rate, return_column),
        "max_drawdown": max_drawdown(data_for_calc, price_column),
    }
    try:
        metrics["var_95"] = var_parametric(data_for_calc, 0.95, return_column)
    except Exception:
        metrics["var_95"] = None
    return metrics
