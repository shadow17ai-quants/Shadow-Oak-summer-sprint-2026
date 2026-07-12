"""
Validation module for SovereignFinance.
Handles input validation for transactions and other data.
"""

import re
from datetime import datetime

from sovfin.config import DATE_FORMAT


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


def validate_category(category: str) -> str:
    """
    Validate and normalize category input.

    Args:
        category: Category string to validate

    Returns:
        str: Validated and normalized category

    Raises:
        ValidationError: If category is invalid
    """
    if not category or not category.strip():
        raise ValidationError("Category cannot be empty")

    cleaned = category.strip()
    if len(cleaned) > 50:
        raise ValidationError("Category must be 50 characters or less")

    # Allow letters, numbers, spaces, and common punctuation
    if not re.match(r"^[a-zA-Z0-9\s\-_.,&]+$", cleaned):
        raise ValidationError(
            "Category contains invalid characters. "
            "Only letters, numbers, spaces, hyphens, underscores, periods, commas, and ampersands are allowed."
        )

    return cleaned


def validate_amount(amount_str: str) -> float:
    """
    Validate and convert amount input.

    Args:
        amount_str: Amount as string to validate

    Returns:
        float: Validated amount

    Raises:
        ValidationError: If amount is invalid
    """
    try:
        amount = float(amount_str)
    except ValueError:
        raise ValidationError("Amount must be a valid number")

    if amount == 0:
        raise ValidationError("Amount cannot be zero")

    # Optional: Add reasonable limits
    if abs(amount) > 1_000_000:  # 1 million
        raise ValidationError("Amount is too large (maximum 1,000,000)")

    return amount


def validate_date(date_str: str) -> str:
    """
    Validate date string format and validity.

    Args:
        date_str: Date string to validate (expected format: YYYY-MM-DD)

    Returns:
        str: Validated date string

    Raises:
        ValidationError: If date is invalid
    """
    if not date_str:
        # Return today's date if empty
        return datetime.now().strftime(DATE_FORMAT)

    try:
        # Validate format
        parsed_date = datetime.strptime(date_str, DATE_FORMAT)
        # Additional validation: check if it's a real date
        formatted_date = parsed_date.strftime(DATE_FORMAT)
        if formatted_date != date_str:
            raise ValueError
        return formatted_date
    except ValueError:
        raise ValidationError(
            f"Invalid date format. Please use {DATE_FORMAT} (YYYY-MM-DD)"
        )


def validate_description(description: str) -> str:
    """
    Validate and sanitize description input.

    Args:
        description: Description string to validate

    Returns:
        str: Validated description (empty string if None or only whitespace)
    """
    if not description:
        return ""

    cleaned = description.strip()
    # Limit length to prevent extremely long descriptions
    if len(cleaned) > 500:
        raise ValidationError("Description must be 500 characters or less")

    return cleaned


def validate_transaction_data(
    category: str, amount_str: str, date_str: str, description: str = ""
) -> tuple:
    """
    Validate all transaction data at once.

    Args:
        category: Transaction category
        amount_str: Amount as string
        date_str: Date string
        description: Transaction description

    Returns:
        tuple: (category, amount, date, description) - all validated and processed

    Raises:
        ValidationError: If any validation fails
    """
    validated_category = validate_category(category)
    validated_amount = validate_amount(amount_str)
    validated_date = validate_date(date_str)
    validated_description = validate_description(description)

    return validated_category, validated_amount, validated_date, validated_description
