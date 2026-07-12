"""
Tests for the seed_data script.
"""

import importlib
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest


def test_seed_data_script_exists():
    """Test that the seed_data.py script exists."""
    script_path = Path(__file__).parent.parent / "seed_data.py"
    assert script_path.exists()
    assert script_path.is_file()


def test_seed_data_creates_tables_and_data():
    """Test that running seed_data creates tables and inserts data."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_db_path = tmp_path / "test_finance.db"

        # Set environment variable to override DB path
        os.environ["SEED_DB_PATH"] = str(test_db_path)

        # Ensure the directory containing seed_data.py is on sys.path
        sys.path.insert(0, str(Path(__file__).parent.parent))

        # Import the module (it may have been imported already, so reload)
        if "seed_data" in sys.modules:
            seed_data = importlib.reload(sys.modules["seed_data"])
        else:
            import seed_data

        # Run the main function
        seed_data.main()

        # Check that the database file was created
        assert test_db_path.exists()

        # Check that the database has the expected tables and data
        with sqlite3.connect(test_db_path) as conn:
            cursor = conn.cursor()

            # Check that transactions table exists
            cursor.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='transactions'
            """
            )
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == "transactions"

            # Check that we have data
            cursor.execute("SELECT COUNT(*) FROM transactions")
            count = cursor.fetchone()[0]
            assert count == 15  # 5 incomes + 10 expenses from seed_data.py

            # Check a few sample records
            cursor.execute("SELECT category, amount, date FROM transactions LIMIT 3")
            rows = cursor.fetchall()
            assert len(rows) == 3

            # All categories should be from our predefined lists
            categories = [row[0] for row in rows]
            valid_incomes = ["Salary", "Freelance", "Bonus", "Dividend", "Refund"]
            valid_expenses = ["Rent", "Food", "Transport", "Entertainment", "Utilities"]
            for category in categories:
                assert category in valid_incomes or category in valid_expenses

        # Clean up environment variable
        del os.environ["SEED_DB_PATH"]


if __name__ == "__main__":
    pytest.main([__file__])
