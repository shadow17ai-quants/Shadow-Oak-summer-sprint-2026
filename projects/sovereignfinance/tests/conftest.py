"""
Shared test configuration and fixtures.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for all tests
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_transaction_data():
    """Provide sample transaction data for tests."""
    return {
        "category": "Salary",
        "amount": 5000.0,
        "date": "2023-01-15",
        "description": "Monthly salary",
    }


@pytest.fixture
def sample_expense_data():
    """Provide sample expense data for tests."""
    return {
        "category": "Food",
        "amount": -25.50,
        "date": "2023-01-16",
        "description": "Lunch at restaurant",
    }


@pytest.fixture
def valid_categories():
    """Provide list of valid categories for testing."""
    return [
        "Salary",
        "Freelance",
        "Bonus",
        "Dividend",
        "Refund",
        "Rent",
        "Food",
        "Transport",
        "Entertainment",
        "Utilities",
    ]


@pytest.fixture
def invalid_categories():
    """Provide list of invalid categories for testing."""
    return ["", "   ", "a" * 51, "Invalid@Char", "Invalid#Char", "Invalid$Char"]


if __name__ == "__main__":
    # This file is meant to be imported by pytest, not run directly
    pass
