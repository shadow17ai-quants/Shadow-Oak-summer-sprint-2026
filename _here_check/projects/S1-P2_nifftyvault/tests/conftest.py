"""
Shared test fixtures.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_price_data():
    """DataFrame with steadily increasing prices."""
    dates = pd.date_range("2023-01-01", periods=10, freq="B")
    prices = [100 + i for i in range(len(dates))]  # 100,101,...
    return pd.DataFrame({"Adj Close": prices}, index=dates)


@pytest.fixture
def sample_returns_data():
    """DataFrame with known returns."""
    dates = pd.date_range("2023-01-01", periods=10, freq="B")
    # constant daily return of 0.001 (0.1%)
    returns = [0.001] * len(dates)
    return pd.DataFrame({"simple_return": returns}, index=dates)
