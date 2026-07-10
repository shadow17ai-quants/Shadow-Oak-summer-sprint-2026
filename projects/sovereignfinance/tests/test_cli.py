"""
Tests for the CLI module.
"""

import pytest
from unittest.mock import patch
import io
import sys

# Add src to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sovfin.cli import main


def test_cli_menu_display():
    """Test that the CLI menu displays correctly."""
    # We'll test this by mocking input to return '5' (exit) immediately
   # and capturing the output
    with patch('builtins.input', return_value='5'):
        with patch('sys.stdout', new_callable=io.StringIO) as m_stdout:
            try:
                main()
            except SystemExit:
                pass  # Expected when option 5 is selected

            output = m_stdout.getvalue()
            # Check that menu elements are present
            assert "SovereignFinance" in output
            assert "1. Add Income" in output
            assert "2. Add Expense" in output
            assert "3. View All Transactions" in output
            assert "4. Generate PDF Report" in output
            assert "5. Exit" in output


def test_cli_add_income_flow():
    """Test the flow for adding an income transaction."""
    # Mock input sequence: Choose option 1, then provide transaction details, then choose option 5 to exit
    inputs = iter([
        '1',  # Choose Add Income
        'Salary',  # Category
        '5000.00',  # Amount
        '2023-01-15',  # Date
        'Monthly salary',  # Description
        '5'  # Exit
    ])

    with patch('builtins.input', lambda _: next(inputs)):
        with patch('sovfin.cli.db.add_transaction') as mock_add:
            mock_add.return_value = 1  # Return a fake ID
            with patch('sys.stdout', new_callable=io.StringIO):
                try:
                    main()
                except SystemExit:
                    pass  # Expected when option 5 is selected

    # Verify that add_transaction was called with correct parameters
    mock_add.assert_called_once_with(
        category="Salary",
        amount=5000.0,
        date="2023-01-15",
        description="Monthly salary"
    )