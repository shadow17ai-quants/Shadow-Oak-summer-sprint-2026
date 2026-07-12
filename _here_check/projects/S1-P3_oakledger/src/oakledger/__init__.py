"""
OakLedger ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ Trading Journal
A simple trading journal for logging and analysing paper trades.
"""

# Package metadata
__title__ = "OakLedger"
__description__ = "Trading journal for logging and analysing paper trades"
__version__ = "0.1.0"
__author__ = "Shadow Oak Capitals"
__license__ = "MIT"

# Import submodules to make them available at package level
from oakledger import analytics, cli, dashboard

# Key exports for easy access
from oakledger.analytics import behavioral_metrics, compute_metrics, load_trades
from oakledger.cli import main as cli_main

try:
    from .dashboard import main as dashboard_main  # type: ignore[attr-defined]
except ImportError:
    dashboard_main = None

# Define what gets imported with "from oakledger import *"
__all__ = [
    # Metadata
    "__title__",
    "__description__",
    "__version__",
    "__author__",
    "__license__",
    # Submodules
    "analytics",
    "cli",
    "dashboard",
    # Analytics
    "load_trades",
    "compute_metrics",
    "behavioral_metrics",
    # CLI
    "cli_main",
    # Dashboard (optional)
    # "dashboard_main",
]
