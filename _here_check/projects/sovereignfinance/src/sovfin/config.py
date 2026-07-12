"""
Configuration module for SovereignFinance.
Centralized configuration management.
"""

import os
from pathlib import Path
from typing import Final

# Base directories
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Database configuration
DATABASE_NAME: Final[str] = "finance.db"
DATABASE_PATH: Final[Path] = DATA_DIR / DATABASE_NAME

# Logging configuration
LOG_LEVEL: Final[int] = (
    getattr(__import__("logging"), os.getenv("LOG_LEVEL", "INFO").upper())
    if os.getenv("LOG_LEVEL")
    else 20  # logging.INFO
)
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE: Final[Path] = LOGS_DIR / "sovereignfinance.log"

# Date format constants
DATE_FORMAT: Final[str] = "%Y-%m-%d"
DISPLAY_DATE_FORMAT: Final[str] = "%b %d, %Y"

# Application metadata
APP_NAME: Final[str] = "SovereignFinance"
APP_VERSION: Final[str] = "1.0.0"
APP_DESCRIPTION: Final[str] = "Personal Finance Tracker for Shadow Oak Capitals"

# PDF report configuration
PDF_REPORT_DIR: Final[Path] = PROJECT_ROOT / "reports"
PDF_REPORT_DIR.mkdir(exist_ok=True)
PDF_FILENAME_PATTERN: Final[str] = "finance_report_{timestamp}.pdf"
PDF_DPI: Final[int] = 300
PDF_FIGSIZE: Final[tuple] = (12, 8)

# Validation constants
MAX_CATEGORY_LENGTH: Final[int] = 50
MAX_DESCRIPTION_LENGTH: Final[int] = 500
MAX_AMOUNT_LIMIT: Final[float] = 1_000_000.0

# Chart configuration
CHART_COLORS: Final[dict] = {
    "positive": "#2E8B57",  # Sea Green
    "negative": "#DC143C",  # Crimson
    "neutral": "#4682B4",  # Steel Blue
    "background": "#FFFFFF",  # White
    "grid": "#E0E0E0",  # Light Gray
}
