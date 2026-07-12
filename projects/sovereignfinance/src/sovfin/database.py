"""
Database module for SovereignFinance.
Handles all database operations with proper connection management and error handling.
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, ContextManager, Dict, List, Optional

from sovfin.config import DATABASE_PATH, LOG_LEVEL

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


class Database:
    """Database connection manager and query executor."""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self) -> None:
        """Ensure the database directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Database path: {self.db_path}")

    @contextmanager
    def get_connection(self) -> ContextManager[sqlite3.Connection]:
        """
        Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection

        Raises:
            DatabaseError: If connection fails
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            # Enable foreign key>
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Database operation failed: {e}") from e
        finally:
            if conn:
                conn.close()

    def initialize_schema(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT
                )
            """)
            conn.commit()
            logger.info("Database schema initialized")

    def add_transaction(self, category: str, amount: float, date: str,
                       description: str = "") -> int:
        """
        Add a new transaction to the database.

        Args:
            category: Transaction category
            amount: Transaction amount (positive for income, negative for expenses)
            date: Date in YYYY-MM-DD format
            description: Optional transaction description

        Returns:
            int: ID of the inserted transaction

        Raises:
            DatabaseError: DatabaseError"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (category, amount, date, description)
                VALUES (?, ?, ?, ?)
            """, (category, amount, date, description))
            conn.commit()
            transaction_id = cursor.lastrowid
            logger.info(f"Transaction added with ID: {transaction_id}")
            return transaction_id

    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """
        Retrieve all transactions ordered by date.

        Returns:
            List of dictionaries representing transactions
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, category, amount, date, description
                FROM transactions
                ORDER BY date
            """)
            rows = cursor.fetchall()

            # Convert to list of dictionaries
            columns = [description[0] for description in cursor.description]
            transactions = []
            for row in rows:
                transaction = dict(zip(columns, row))
                transactions.append(transaction)

            return transactions

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete a transaction by ID.

        Args:
            transaction_id: ID of the transaction to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
            rows_affected = cursor.rowcount

            if rows_affected > 0:
                logger.info(f"Transaction {transaction_id} deleted")
                return True
            else:
                logger.warning(f"No transaction found with ID: {transaction_id}")
                return False

    def update_transaction(self, transaction_id: int, category: str, amount: float,
                          date: str, description: str = "") -> bool:
        """
        Update an existing transaction.

        Args:
            transaction_id: ID of the transaction to update
            category: New category
            amount: New amount
            date: New date in YYYY-MM-DD format
            description: New description

        Returns:
            bool: True if update was successful, False otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET category = ?, amount = ?, date = ?, description = ?
                WHERE id = ?
            """, (category, amount, date, description, transaction_id))
            conn.commit()
            rows_affected = cursor.rowcount

            if rows_affected > 0:
                logger.info(f"Transaction {transaction_id} updated")
                return True
            else:
                logger.warning(f"No transaction found with ID: {transaction_id}")
                return False

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a transaction by its ID.

        Args:
            transaction_id: ID of the transaction to retrieve

        Returns:
            Dictionary representing the transaction, or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, category, amount, date, description
                FROM transactions
                WHERE id = ?
            """, (transaction_id,))
            row = cursor.fetchone()

            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None


# Global database instance
db = Database()
