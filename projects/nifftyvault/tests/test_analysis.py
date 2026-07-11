"""
Tests for the analysis module.
"""

import numpy as np
import pandas as pd
import pytest

from nifftyvault.analysis import (
    annualized_return,
    annualized_volatility,
    calculate_all_metrics,
    max_drawdown,
    sharpe_ratio,
)


@pytest.fixture
def sample_price_data():
    """Create a small sample price DataFrame."""
    dates = pd.date_range("2023-01-01", periods=10, freq="B")
    # simple upward trend with some noise
    prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    df = pd.DataFrame({"Adj Close": prices}, index=dates)
    return df


@pytest.fixture
def sample_returns_data():
    """Create a DataFrame with known returns."""
    dates = pd.date_range("2023-01-01", periods=10, freq="B")
    # 1% daily return
    returns = [0.01] * 10
    df = pd.DataFrame({"simple_return": returns}, index=dates)
    return df


def test_annualized_return(sample_returns_data):
    # daily mean = 0.01, annualized ~ (1.01)^252 - 1
    expected = (1 + 0.01) ** 252 - 1
    result = annualized_return(sample_returns_data)
    assert np.isclose(result, expected, rtol=1e-4)


def test_annualized_volatility(sample_returns_data):
    # daily std = 0 (since constant return), annualized vol = 0
    result = annualized_volatility(sample_returns_data)
    assert np.isclose(result, 0.0)


def test_sharpe_ratio_zero_riskfree(sample_returns_data):
    # excess return = annual return, vol = 0 -> infinite or division by zero?
    # Since volatility zero, Sharpe ratio is infinite (or undefined). Our function
    # will produce division by zero -> returns inf? Let's check implementation.
    # In our implementation, ann_vol = 0, then division yields inf.
    result = sharpe_ratio(sample_returns_data, risk_free_rate=0.0)
    assert np.isinf(result)


def test_max_drawdown(sample_price_data):
    # With monotonically increasing prices, max drawdown should be 0 (no loss)
    result = max_drawdown(sample_price_data)
    assert np.isclose(result, 0.0)


def test_calculate_all_metrics(sample_price_data):
    metrics = calculate_all_metrics(sample_price_data)
    # check that keys exist
    assert "annualized_return" in metrics
    assert "annualized_volatility" in metrics
    assert "sharpe_ratio" in metrics
    assert "sortino_ratio" in metrics
    assert "max_drawdown" in metrics
    assert "var_95" in metrics
