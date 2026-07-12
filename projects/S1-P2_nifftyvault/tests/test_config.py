"""
Tests for the configuration module.
"""

from pathlib import Path

from nifftyvault.config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    CHART_COLOR,
    CHART_DPI,
    CHART_FIGSIZE,
    CHART_STYLE,
    CONFIDENCE_LEVEL,
    DATA_DIR,
    DEFAULT_CHART_FILE,
    DEFAULT_DATA_FILE,
    DEFAULT_METRICS_FILE,
    DEFAULT_PERIOD_YEARS,
    DEFAULT_RISK_FREE_RATE,
    DEFAULT_TICKER,
    MAX_PERIOD_YEARS,
    MIN_PERIOD_YEARS,
    PROJECT_ROOT,
    TRADING_DAYS_PER_YEAR,
)


def test_config_imports():
    """Ensure all expected constants are accessible."""
    assert DEFAULT_TICKER == "^NSEI"
    assert DEFAULT_PERIOD_YEARS == 5
    assert TRADING_DAYS_PER_YEAR == 252

    assert isinstance(DEFAULT_DATA_FILE, Path)
    assert DEFAULT_DATA_FILE == DATA_DIR / "nifty_50_data.csv"

    assert isinstance(DEFAULT_METRICS_FILE, Path)
    assert DEFAULT_METRICS_FILE == PROJECT_ROOT / "nifty_metrics.txt"

    assert isinstance(DEFAULT_CHART_FILE, Path)
    assert DEFAULT_CHART_FILE == PROJECT_ROOT / "nifty_50_price_chart.png"

    assert MIN_PERIOD_YEARS == 1
    assert MAX_PERIOD_YEARS == 20

    assert DEFAULT_RISK_FREE_RATE == 0.0
    assert CONFIDENCE_LEVEL == 0.95

    assert CHART_FIGSIZE == (12, 6)
    assert CHART_DPI == 150
    assert CHART_STYLE == "default"
    assert CHART_COLOR == "#1f77b4"

    assert APP_NAME == "NifftyVault"
    assert APP_VERSION == "0.1.0"
    assert APP_DESCRIPTION == "Nifty 50 Data Analyzer for Shadow Oak Capitals"
