"""
Command-line interface for SovereignFinance.
Provides a menu-driven CLI for managing personal finances.
"""

import logging
from datetime import datetime
from typing import NoReturn

from sovfin.config import APP_NAME, APP_VERSION, LOG_FORMAT, LOG_LEVEL
from sovfin.database import db
from sovfin.validation import ValidationError, validate_transaction_data

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),  # Console output
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"{APP_NAME} v{APP_VERSION} starting up")


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "="*50)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print("="*50)
    print("  1. Add Income")
    print("  2. Add Expense")
    print("  3. View All Transactions")
    print("  4. Generate PDF Report")
    print("  5. Exit")
    print("-"*50)


def get_transaction_details(is_income: bool = True) -> tuple:
    """
    Get transaction details from user input with validation.

    Args:
        is_income: True for income, False for expense

    Returns:
        tuple: (category, amount, date, description)
    """
    transaction_type = "Income" if is_income else "Expense"
    print(f"\n--- Add {transaction_type} ---")

    while True:
        try:
            category = input("Category (e.g., Salary, Rent, Food): ").strip()
            amount_str = input("Amount (): ").strip()
            date_str = input(
                "Date (YYYY-MM-DD, press Enter for today): "
            ).strip()
            description = input("Description (optional): ").strip()

            # Validate all inputs
            category, amount, date, description = validate_transaction_data(
                category, amount_str, date_str, description
            )

            # Adjust amount sign based on transaction type
            if not is_income:  # Expense
                amount = -abs(amount)
            else:  # Income
                amount = abs(amount)

            return category, amount, date, description

        except ValidationError as e:
            print(f" Validation error: {e}")
            print("Please try again.\n")
        except Exception as e:
            logger.error(f"Unexpected error getting transaction details: {e}")
            print(" An unexpected error occurred. Please try again.")


def add_transaction(is_income: bool = True) -> None:
    """
    Add a transaction (income or expense) to the database.

    Args:
        is_income: True for income, False for expense
    """
    try:
        category, amount, date, description = get_transaction_details(is_income)
        transaction_id = db.add_transaction(category=category, amount=amount, date=date, description=description)
        transaction_type = "Income" if is_income else "Expense"
        print(f" {transaction_type} added successfully! (ID: {transaction_id})")
        logger.info(f"{transaction_type} added: {category} | {amount:,.2f} | {date}")

    except Exception as e:
        logger.error(f"Failed to add transaction: {e}")
        print(" Failed to add transaction. Please check the logs for details.")


def view_all_transactions() -> None:
    """Display all transactions in a formatted table."""
    try:
        transactions = db.get_all_transactions()

        if not transactions:
            print("\n No transactions found.")
            return

        print("\n" + "="*80)
        print(f"{'ID':<4} {'Category':<20} {'Amount':>12} {'Date':<12} {'Description'}")
        print("-"*80)

        total_income = 0.0
        total_expense = 0.0

        for t in transactions:
            amount = t['amount']
            if amount >= 0:
                total_income += amount
            else:
                total_expense += abs(amount)

            # Format amount with color indicators (in terminal that supports it)
            amount_str = f"₹{amount:,.2f}"
            print(
                f"{t['id']:<4} "
                f"{t['category']:<20} "
                f"{amount_str:>12} "
                f"{t['date']:<12} "
                f"{t['description'] or ''}"
            )

        print("="*80)
        print(f"Total Income:  {total_income:,.2f}")
        print(f"Total Expense: {total_expense:,.2f}")
        print(f"Net Balance:   {total_income - total_expense:,.2f}")
        print(f"Transaction Count: {len(transactions)}")

    except Exception as e:
        logger.error(f"Failed to retrieve transactions: {e}")
        print(" Failed to load transactions. Please check the logs for details.")


def generate_pdf_report() -> None:
    """Generate a PDF report with income/expense charts and cumulative balance."""
    try:
        # Import here to avoid slowing down CLI if matplotlib isn't used
        import matplotlib.pyplot as plt

        from .config import (
            CHART_COLORS,
            PDF_DPI,
            PDF_FIGSIZE,
            PDF_FILENAME_PATTERN,
            PDF_REPORT_DIR,
        )

        transactions = db.get_all_transactions()

        if not transactions:
            print("\n No data to generate report. Add some transactions first.")
            return

        # Prepare data
        categories = {}
        dates = []
        balances = []
        running_balance = 0

        for t in transactions:
            category = t['category']
            amount = t['amount']
            date = t['date']

            # Accumulate by category
            categories[category] = categories.get(category, 0) + amount

            # For cumulative balance
            dates.append(date)
            running_balance += amount
            balances.append(running_balance)

        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=PDF_FIGSIZE)
        fig.suptitle(f"{APP_NAME} Financial Report", fontsize=16, fontweight='bold')

        # ---- Bar chart: Income vs Expense by Category ----
        cats = list(categories.keys())
        amounts = list(categories.values())
        colors = [
            CHART_COLORS["positive"] if x >= 0 else CHART_COLORS["negative"]
            for x in amounts
        ]

        bars = ax1.bar(cats, amounts, color=colors, edgecolor='black', linewidth=0.8)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax1.set_title("Income vs Expense by Category", fontsize=14, fontweight='bold')
        ax1.set_ylabel("Amount ()", fontsize=12)
        ax1.set_xlabel("Category", fontsize=12)

        # Add value labels on bars
        for bar, amount in zip(bars, amounts):
            height = bar.get_height()
            label_y = height + (100 if height >= 0 else -300)
            ax1.text(
                bar.get_x() + bar.get_width()/2,
                label_y,
                f"{amount:,.0f}",
                ha='center', va='bottom' if height >= 0 else 'top',
                fontsize=9, fontweight='bold'
            )

        ax1.tick_params(axis='x', rotation=45)

        # ---- Line chart: Cumulative Balance ----
        ax2.plot(dates, balances, marker='o', linestyle='-',
                color=CHART_COLORS["neutral"], linewidth=2, markersize=4)
        ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
        ax2.set_title("Cumulative Balance Over Time", fontsize=14, fontweight='bold')
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("Balance ()", fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = PDF_FILENAME_PATTERN.format(timestamp=timestamp)
        pdf_path = PDF_REPORT_DIR / pdf_filename

        plt.savefig(pdf_path, dpi=PDF_DPI, bbox_inches='tight', facecolor='white')
        plt.close(fig)

        print("\n PDF report generated successfully!")
        print(f"   Location: {pdf_path.absolute()}")
        print(f"   Filename: {pdf_filename}")

        logger.info(f"PDF report generated: {pdf_path}")

    except ImportError:
        logger.error("Matplotlib not available for PDF generation")
        print(" Unable to generate PDF report. matplotlib is not installed.")
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {e}")
        print(" Failed to generate PDF report. Please check the logs for details.")


def main() -> NoReturn:
    """Main CLI application loop."""
    # Initialize database schema
    try:
        db.initialize_schema()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize database: {e}")
        print(" Critical error: Unable to initialize database. Exiting.")
        return

    print(f" Welcome to {APP_NAME}!")
    print("   Shadow Oak Capitals - Personal Finance Tracker")

    while True:
        try:
            display_menu()
            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                add_transaction(is_income=True)  # Income
            elif choice == "2":
                add_transaction(is_income=False)  # Expense
            elif choice == "3":
                view_all_transactions()
            elif choice == "4":
                generate_pdf_report()
            elif choice == "5":
                print("\n Thank you for using SovereignFinance!")
                print("   Keep building your financial record.")
                logger.info("Application exited by user")
                break
            else:
                print(" Invalid option. Please choose 1-5.")

        except KeyboardInterrupt:
            print("\n\n Application interrupted. Goodbye!")
            logger.info("Application interrupted by user (KeyboardInterrupt)")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            print(" An unexpected error occurred. Please check the logs.")


if __name__ == "__main__":
    main()
