"""
Tests for the dashboard module.
"""

import pytest
from unittest.mock import patch, MagicMock

# Add src to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_dashboard_imports():
    """Test that the dashboard module can be imported without errors."""
    try:
        from sovfin.dashboard import main
        assert callable(main)
    except ImportError as e:
        pytest.fail(f"Failed to import dashboard module: {e}")


def test_dashboard_main_function_exists():
    """Test that the dashboard has a main function."""
    from sovfin.dashboard import main
    assert callable(main)


def test_dashboard_page_config():
    """Test that dashboard sets up page configuration correctly."""
    # We can't easily test the actual Streamlit page config without running the app,
    # but we can verify that the st.set_page_config call exists in the source
    import inspect
    import sovfin.dashboard

    source = inspect.getsource(sovfin.dashboard)
    assert "st.set_page_config" in source
    assert "page_title" in source
    assert "page_icon" in source
    assert "layout" in source


def test_dashboard_has_expected_functions():
    """Test that dashboard has all expected UI functions."""
    from sovfin.dashboard import (
        show_summary_page,
        show_transactions_page,
        show_charts_page,
        show_add_transaction_page,
        show_manage_page
    )

    assert callable(show_summary_page)
    assert callable(show_transactions_page)
    assert callable(show_charts_page)
    assert callable(show_add_transaction_page)
    assert callable(show_manage_page)


def test_dashboard_database_initialization():
    """Test that dashboard initializes database on startup."""
    # We can't easily test the actual database initialization without mocking streamlit
    # but we can verify that the code calls db.initialize_schema()
    import inspect
    import sovfin.dashboard

    source = inspect.getsource(sovfin.dashboard)
    assert "db.initialize_schema()" in source


if __name__ == "__main__":
    pytest.main([__file__])