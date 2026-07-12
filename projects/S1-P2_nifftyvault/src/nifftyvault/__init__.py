"""
NifftyVault - Nifty 50 Data Analyzer
A quantitative data pipeline for analyzing Nifty 50 market data.
"""

# Package metadata
__title__ = "NifftyVault"
__description__ = "Nifty 50 Data Analyzer for Shadow Oak Capitals"
__version__ = "0.1.0"
__author__ = "Shadow Oak Capitals"
__license__ = "Proprietary"

# Key exports for easy access
from . import analysis, config, data, visualization
from .analysis import (
    annualized_return,
    annualized_volatility,
    calculate_all_metrics,
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
    var_parametric,
)
from .config import (
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
    TRADING_DAYS_PER_YEAR,
)
from .data import NiftyDataManager, download_nifty_50, load_nifty_50_data
from .visualization import (
    plot_cumulative_returns,
    plot_price_history,
    plot_returns_distribution,
    plot_rolling_metrics,
)

# Define what gets imported with "from nifftyvault import *"
__all__ = [
    # Metadata
    "__title__",
    "__description__",
    "__version__",
    "__author__",
    "__license__",
    # Submodules
    "analysis",
    "config",
    "data",
    "visualization",
    # Config
    "DATA_DIR",
    "DEFAULT_TICKER",
    "DEFAULT_PERIOD_YEARS",
    "TRADING_DAYS_PER_YEAR",
    "DEFAULT_DATA_FILE",
    "DEFAULT_METRICS_FILE",
    "DEFAULT_CHART_FILE",
    MIN_PERIOD_YEARS,
    MAX_PERIOD_YEARS,
    "DEFAULT_RISK_FREE_RATE",
    "CONFIDENCE_LEVEL",
    "CHART_FIGSIZE",
    "CHART_DPI",
    "CHART_STYLE",
    "CHART_COLOR",
    "APP_NAME",
    "APP_VERSION",
    "APP_DESCRIPTION",
    # Data
    "NiftyDataManager",
    "download_nifty_50",
    "load_nifty_50_data",
    # Analysis
    "annualized_return",
    "annualized_volatility",
    "sharpe_ratio",
    "sortino_ratio",
    "max_drawdown",
    "var_parametric",
    "calculate_all_metrics",
    # Visualization
    "plot_price_history",
    "plot_returns_distribution",
    "plot_cumulative_returns",
    "plot_rolling_metrics",
]
