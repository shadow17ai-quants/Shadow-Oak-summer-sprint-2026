"""
Tests for the validation module.
"""

import pytest
from datetime import datetime

# Add src to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sovfin.validation import (
    validate_category,
    validate_amount,
    validate_date,
    validate_description,
    validate_transaction_data,
    ValidationError
)


def test_validate_category_valid():
    """Test validation of valid categories."""
    # Test normal category
    assert validate_category("Salary") == "Salary"
    assert validate_category("Food & Dining") == "Food & Dining"
    assert validate_category("Home_Office") == "Home_Office"
    assert validate_category("Transport-2023") == "Transport-2023"

    # Test with whitespace (should be stripped)
    assert validate_category("  Salary  ") == "Salary"
    assert validate_category("\t\nFood\n\t") == "Food"

    # Test maximum length (50 characters)
    max_category = "a" * 50
    assert validate_category(max_category) == max_category


def test_validate_category_invalid():
    """Test validation of invalid categories."""
    # Test empty string
    with pytest.raises(ValidationError, match="Category cannot be empty"):
        validate_category("")

    # Test only whitespace
    with pytest.raises(ValidationError, match="Category cannot be empty"):
        validate_category("   ")

    with pytest.raises(ValidationError, match="Category cannot be empty"):
        validate_category("\n\t")

    # Test too long
    with pytest.raises(ValidationError, match="Category must be 50 characters or less"):
        validate_category("a" * 51)

    # Test invalid characters
    with pytest.raises(ValidationError, match="Category contains invalid characters"):
        validate_category("Salary@")  # @ not allowed

    with pytest.raises(ValidationError, match="Category contains invalid characters"):
        validate_category("Food #1")  # # not allowed

    with pytest.raises(ValidationError, match="Category contains invalid characters"):
        validate_category("Home$")  # $ not allowed


def test_validate_amount_valid():
    """Test validation of valid amounts."""
    # Test integers
    assert validate_amount("100") == 100.0
    assert validate_amount("1") == 1.0

    # Test floats
    assert validate_amount("100.50") == 100.50
    assert validate_amount("0.99") == 0.99
    assert validate_amount("100.0") == 100.0

    # Test negative numbers (these are valid amounts - sign indicates expense/income)
    assert validate_amount("-50.25") == -50.25
    assert validate_amount("-100") == -100.0

    # Test scientific notation (float() handles this)
    assert validate_amount("1e2") == 100.0
    assert validate_amount("1.5e2") == 150.0


def test_validate_amount_invalid():
    """Test validation of invalid amounts."""
    # Test zero amount (not allowed)
    with pytest.raises(ValidationError, match="Amount cannot be zero"):
        validate_amount("0")

    with pytest.raises(ValidationError, match="Amount cannot be zero"):
        validate_amount("0.0")

    with pytest.raises(ValidationError, match="Amount cannot be zero"):
        validate_amount("-0")

    # Test non-numeric strings
    with pytest.raises(ValidationError, match="Amount must be a valid number"):
        validate_amount("abc")

    with pytest.raises(ValidationError, match="Amount must be a valid number"):
        validate_amount("100abc")

    with pytest.raises(ValidationError, match="Amount must be a valid number"):
        validate_amount("")

    with pytest.raises(ValidationError, match="Amount must be a valid number"):
        validate_amount("   ")

    # Test amount too large
    with pytest.raises(ValidationError, match="Amount is too large"):
        validate_amount("1000000.01")  # Just over the limit

    with pytest.raises(ValidationError, match="Amount is too large"):
        validate_amount("1000001")


def test_validate_date_valid():
    """Test validation of valid dates.
    """
    # Test normal dates
    assert validate_date("2023-01-15") == "2023-01-15"
    assert validate_date("2023-12-31") == "2023-12-31"
    assert validate_date("2020-02-29") == "2020-02-29"  # Leap year

    # Test empty date (should return today's date)
    today = datetime.now().strftime("%Y-%m-%d")
    assert validate_date("") == today
    assert validate_date(None) == today  # None should be treated as empty


def test_validate_date_invalid():
    """Test validation of invalid dates."""
    # Test invalid format
    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023/01/15")  # Wrong separator

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("15-01-2023")  # Wrong order

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("Jan 15, 2023")  # Text format

    # Test invalid dates
    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023-02-29")  # Non-leap year

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023-13-01")  # Invalid month

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023-00-01")  # Invalid month

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023-01-32")  # Invalid day

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023-01-00")  # Invalid day

    # Test malformed strings
    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("not-a-date")

    with pytest.raises(ValidationError, match="Invalid date format"):
        validate_date("2023-01")


def test_validate_description_valid():
    """Test validation of valid descriptions."""
    # Test normal description
    assert validate_description("Regular description") == "Regular description"

    # Test empty description (should return empty string)
    assert validate_description("") == ""
    assert validate_description(None) == ""

    # Test whitespace only (should be stripped to empty string)
    assert validate_description("   ") == ""
    assert validate_description("\n\t") == ""

    # Test maximum length (500 characters)
    max_description = "a" * 500
    assert validate_description(max_description) == max_description

    # Test with newlines and tabs (should be preserved but stripped of leading/trailing whitespace)
    desc_with_whitespace = "  \n\t  Hello World  \n\t  "
    assert validate_description(desc_with_whitespace) == "Hello World"


def test_validate_description_invalid():
    """Test validation of invalid descriptions."""
    # Test too long
    with pytest.raises(ValidationError, match="Description must be 500 characters or less"):
        validate_description("a" * 501)


def test_validate_transaction_data_valid():
    """Test validation of valid transaction data."""
    # Just test that it doesn't throw an exception for valid input
    try:
        validate_transaction_data("Salary", "100.0", "2023-01-15", "Test")
    except Exception as e:
        pytest.fail(f"validate_transaction_data raised {type(e).__name__} unexpectedly: {e}")


def test_validate_transaction_data_invalid_category():
    """Test validation with invalid category."""
    with pytest.raises(ValidationError, match="Category cannot be empty"):
        validate_transaction_data("", "100.0", "2023-01-15")


if __name__ == "__main__":
    pytest.main([__file__])