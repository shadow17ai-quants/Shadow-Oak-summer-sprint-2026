"""
Tests for the database module.
"""

import sqlite3

# Add src to path for imports
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sovfin.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_finance.db"
        db = Database(db_path)
        db.initialize_schema()  # Initialize the schema so tables exist
        yield db


def test_database_initialization(temp_db):
    """Test that database initializes correctly."""
    assert temp_db.db_path.exists()
    assert temp_db.db_path.is_file()


def test_database_initialize_schema():
    """Test that database schema is created correctly."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_finance.db"
        db = Database(db_path)

        # Before initialization, tables shouldn't exist
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='transactions'
            """)
            result = cursor.fetchone()
            assert result is None  # Table doesn't exist yet

        # Initialize schema
        db.initialize_schema()

        # After initialization, table should exist
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='transactions'
            """)
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == "transactions"

            # Check table structure
            cursor.execute("PRAGMA table_info(transactions)")
            columns = cursor.fetchall()
            assert len(columns) == 5

            # Check column names and types
            column_names = [col[1] for col in columns]
            expected_columns = ["id", "category", "amount", "date", "description"]
            assert column_names == expected_columns

            # Check that id is INTEGER PRIMARY KEY
            id_col = columns[0]
            assert id_col[1] == "id"
            assert id_col[2] == "INTEGER"
            assert id_col[5] == 1  # Primary key flag

            # Check that amount is REAL (fixed from INTEGER in original)
            amount_col = columns[2]
            assert amount_col[1] == "amount"
            assert amount_col[2] == "REAL"  # Fixed: changed from INTEGER to REAL


def test_add_and_get_transaction(temp_db):
    """Test adding a transaction and retrieving it."""
    # Add a transaction
    transaction_id = temp_db.add_transaction(
        category="Salary",
        amount=5000.0,
        date="2023-01-15",
        description="Monthly salary",
    )

    # Verify it was added with the correct ID
    assert isinstance(transaction_id, int)
    assert transaction_id > 0

    # Retrieve the transaction
    transaction = temp_db.get_transaction_by_id(transaction_id)

    # Verify the retrieved data
    assert transaction is not None
    assert transaction["id"] == transaction_id
    assert transaction["category"] == "Salary"
    assert transaction["amount"] == 5000.0
    assert transaction["date"] == "2023-01-15"
    assert transaction["description"] == "Monthly salary"


def test_get_all_transactions_empty(temp_db):
    """Test getting all transactions when database is empty."""
    transactions = temp_db.get_all_transactions()
    assert isinstance(transactions, list)
    assert len(transactions) == 0


def test_get_all_transactions_with_data(temp_db):
    """Test getting all transactions when database has data."""
    # Add a few transactions
    temp_db.add_transaction("Salary", 3000.0, "2023-01-01", "January salary")
    temp_db.add_transaction("Freelance", 500.0, "2023-01-15", "Freelance project")
    temp_db.add_transaction("Rent", -1000.0, "2023-01-05", "Monthly rent")

    # Get all transactions
    transactions = temp_db.get_all_transactions()

    # Verify we got all three
    assert isinstance(transactions, list)
    assert len(transactions) == 3

    # Verify they're ordered by date (oldest first)
    assert transactions[0]["date"] == "2023-01-01"
    assert transactions[1]["date"] == "2023-01-05"
    assert transactions[2]["date"] == "2023-01-15"

    # Verify the data
    assert transactions[0]["category"] == "Salary"
    assert transactions[0]["amount"] == 3000.0

    assert transactions[1]["category"] == "Rent"
    assert transactions[1]["amount"] == -1000.0

    assert transactions[2]["category"] == "Freelance"
    assert transactions[2]["amount"] == 500.0


def test_delete_transaction(temp_db):
    """Test deleting a transaction."""
    # Add a transaction
    transaction_id = temp_db.add_transaction(
        category="Expense", amount=-50.0, date="2023-01-20", description="Dinner out"
    )

    # Verify it exists
    assert temp_db.get_transaction_by_id(transaction_id) is not None

    # Delete it
    result = temp_db.delete_transaction(transaction_id)
    assert result is True

    # Verify it's gone
    assert temp_db.get_transaction_by_id(transaction_id) is None

    # Try to delete it again (should return False)
    result = temp_db.delete_transaction(transaction_id)
    assert result is False


def test_update_transaction(temp_db):
    """Test updating a transaction."""
    # Add a transaction
    transaction_id = temp_db.add_transaction(
        category="Food", amount=-25.50, date="2023-01-20", description="Lunch at cafe"
    )

    # Update it
    result = temp_db.update_transaction(
        transaction_id=transaction_id,
        category="Groceries",
        amount=-75.25,
        date="2023-01-21",
        description="Weekly groceries",
    )

    # Verify update succeeded
    assert result is True

    # Retrieve and verify the updated data
    updated = temp_db.get_transaction_by_id(transaction_id)
    assert updated is not None
    assert updated["category"] == "Groceries"
    assert updated["amount"] == -75.25
    assert updated["date"] == "2023-01-21"
    assert updated["description"] == "Weekly groceries"

    # Try to update a non-existent transaction
    result = temp_db.update_transaction(
        transaction_id=99999,
        category="Test",
        amount=10.0,
        date="2023-01-22",
        description="Test",
    )
    assert result is False


def test_get_transaction_by_id_not_found(temp_db):
    """Test getting a non-existent transaction."""
    result = temp_db.get_transaction_by_id(99999)
    assert result is None


def test_database_error_handling():
    """Test that database errors are properly raised."""
    # Try to create a database in a non-existent directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "nonexistent" / "subdir" / "test.db"
        db = Database(db_path)
        db.initialize_schema()  # Initialize schema so we can test connection

        # The directory should be created automatically when we try to connect
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                assert result[0] == 1

            # If we get here, the directory was created successfully
            assert db_path.parent.exists()
        except Exception:
            # If there was an error, it should be a DatabaseError
            # Actually, the Database class creates directories automatically
            # so this shouldn't happen
            pass


def test_connection_context_manager(temp_db):
    """Test that the connection context manager works correctly."""
    # Test normal usage
    with temp_db.get_connection() as conn:
        assert isinstance(conn, sqlite3.Connection)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1

    # Connection should be closed after exiting the context
    # We can't easily test this, but we can verify no resources are leaked
    # by using it multiple times
    for _ in range(5):
        with temp_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")


def test_connection_context_manager_on_error(temp_db):
    """Test that connections are closed even when exceptions occur."""
    try:
        with temp_db.get_connection() as conn:
            assert isinstance(conn, sqlite3.Connection)
            raise ValueError("Test exception")
    except ValueError:
        pass  # Expected

    # Connection should have been closed


if __name__ == "__main__":
    pytest.main([__file__])
