"""
Configuration module for NifftyVault.
Handles application settings and environment variables.
"""

from pathlib import Path
from typing import Final

# Base directories
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)

# Data configuration
DEFAULT_TICKER: Final[str] = "^NSEI"  # Nifty 50 index
DEFAULT_PERIOD_YEARS: Final[int] = 5
TRADING_DAYS_PER_YEAR: Final[int] = 252

# File paths
DEFAULT_DATA_FILE: Final[Path] = DATA_DIR / "nifty_50_data.csv"
DEFAULT_METRICS_FILE: Final[Path] = PROJECT_ROOT / "nifty_metrics.txt"
DEFAULT_CHART_FILE: Final[Path] = PROJECT_ROOT / "nifty_50_price_chart.png"

# Validation constants
MIN_PERIOD_YEARS: Final[int] = 1
MAX_PERIOD_YEARS: Final[int] = 20

# Analysis defaults
DEFAULT_RISK_FREE_RATE: Final[float] = 0.0  # 0% risk-free rate
CONFIDENCE_LEVEL: Final[float] = 0.95  # 95% confidence interval

# Chart configuration
CHART_FIGSIZE: Final[tuple] = (12, 6)
CHART_DPI: Final[int] = 150
CHART_STYLE: Final[str] = "default"
CHART_COLOR: Final[str] = "#1f77b4"  # matplotlib default blue

# Application metadata
APP_NAME: Final[str] = "NifftyVault"
APP_VERSION: Final[str] = "0.1.0"
APP_DESCRIPTION: Final[str] = "Nifty 50 Data Analyzer for Shadow Oak Capitals"
