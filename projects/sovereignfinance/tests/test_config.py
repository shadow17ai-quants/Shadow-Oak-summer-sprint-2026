"""
Tests for SovereignFinance configuration module.
"""

import os
import pytest
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sovfin.config import (
    PROJECT_ROOT, DATA_DIR, LOGS_DIR,
    DATABASE_NAME, DATABASE_PATH,
    LOG_LEVEL, LOG_FORMAT, LOG_FILE,
    DATE_FORMAT, DISPLAY_DATE_FORMAT,
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    PDF_REPORT_DIR, PDF_FILENAME_PATTERN, PDF_DPI, PDF_FIGSIZE,
    MAX_CATEGORY_LENGTH, MAX_DESCRIPTION_LENGTH, MAX_AMOUNT_LIMIT,
    CHART_COLORS
)


def test_config_directories():
    """Test that directory paths are set correctly."""
    # These should be Path objects
    assert isinstance(PROJECT_ROOT, Path)
    assert isinstance(DATA_DIR, Path)
    assert isinstance(LOGS_DIR, Path)

    # DATA_DIR should be PROJECT_ROOT / "data"
    assert DATA_DIR == PROJECT_ROOT / "data"

    # LOGS_DIR should be PROJECT_ROOT / "logs"
    assert LOGS_DIR == PROJECT_ROOT / "logs"

    # Directories should exist (they were created in __init__)
    assert DATA_DIR.exists()
    assert LOGS_DIR.exists()


def test_config_database():
    """Test database configuration."""
    assert isinstance(DATABASE_NAME, str)
    assert DATABASE_NAME == "finance.db"
    assert isinstance(DATABASE_PATH, Path)
    assert DATABASE_PATH == DATA_DIR / DATABASE_NAME


def test_config_logging():
    """Test logging configuration."""
    # LOG_LEVEL should be an integer logging level
    assert isinstance(LOG_LEVEL, int)
    assert LOG_LEVEL in [10, 20, 30, 40, 50]  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    # LOG_FORMAT should be a string
    assert isinstance(LOG_FORMAT, str)
    assert "%(asctime)s" in LOG_FORMAT
    assert "%(name)s" in LOG_FORMAT
    assert "%(levelname)s" in LOG_FORMAT
    assert "%(message)s" in LOG_FORMAT

    # LOG_FILE should be a Path object
    assert isinstance(LOG_FILE, Path)
    assert LOG_FILE == LOGS_DIR / "sovereignfinance.log"


def test_config_date_formats():
    """Test date format configuration."""
    assert isinstance(DATE_FORMAT, str)
    assert DATE_FORMAT == "%Y-%m-%d"

    assert isinstance(DISPLAY_DATE_FORMAT, str)
    assert DISPLAY_DATE_FORMAT == "%b %d, %Y"


def test_config_app_info():
    """Test application metadata."""
    assert isinstance(APP_NAME, str)
    assert APP_NAME == "SovereignFinance"

    assert isinstance(APP_VERSION, str)
    assert APP_VERSION == "1.0.0"

    assert isinstance(APP_DESCRIPTION, str)
    assert APP_DESCRIPTION == "Personal Finance Tracker for Shadow Oak Capitals"


def test_config_pdf_settings():
    """Test PDF report configuration."""
    assert isinstance(PDF_REPORT_DIR, Path)
    assert PDF_REPORT_DIR == PROJECT_ROOT / "reports"
    assert PDF_REPORT_DIR.exists()  # Should be created in __init__

    assert isinstance(PDF_FILENAME_PATTERN, str)
    assert PDF_FILENAME_PATTERN == "finance_report_{timestamp}.pdf"

    assert isinstance(PDF_DPI, int)
    assert PDF_DPI == 300

    assert isinstance(PDF_FIGSIZE, tuple)
    assert len(PDF_FIGSIZE) == 2
    assert PDF_FIGSIZE == (12, 8)


def test_config_validation_constants():
    """Test validation constants."""
    assert isinstance(MAX_CATEGORY_LENGTH, int)
    assert MAX_CATEGORY_LENGTH == 50

    assert isinstance(MAX_DESCRIPTION_LENGTH, int)
    assert MAX_DESCRIPTION_LENGTH == 500

    assert isinstance(MAX_AMOUNT_LIMIT, float)
    assert MAX_AMOUNT_LIMIT == 1_000_000.0


def test_config_chart_colors():
    """Test chart colors configuration."""
    assert isinstance(CHART_COLORS, dict)
    assert "positive" in CHART_COLORS
    assert "negative" in CHART_COLORS
    assert "neutral" in CHART_COLORS
    assert "background" in CHART_COLORS
    assert "grid" in CHART_COLORS

    # Check that they are valid hex colors
    import re
    hex_color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
    for color_name, color_value in CHART_COLORS.items():
        assert isinstance(color_value, str)
        assert hex_color_pattern.match(color_value), f"Invalid color for {color_name}: {color_value}"


def test_environment_variable_override():
    """Test that environment variables can override settings."""
    # Save original values
    original_log_level = os.environ.get("LOG_LEVEL")

    try:
        # Set environment variable
        os.environ["LOG_LEVEL"] = "DEBUG"

        # Reload the module to pick up the new environment variable
        import importlib
        import sovfin.config
        importlib.reload(sovfin.config)

        # Check that the new value was used
        assert sovfin.config.LOG_LEVEL == 10  # DEBUG level

    finally:
        # Restore original environment
        if original_log_level is None:
            os.environ.pop("LOG_LEVEL", None)
        else:
            os.environ["LOG_LEVEL"] = original_log_level

        # Reload again to restore original settings
        import importlib
        import sovfin.config
        importlib.reload(sovfin.config)


if __name__ == "__main__":
    pytest.main([__file__])