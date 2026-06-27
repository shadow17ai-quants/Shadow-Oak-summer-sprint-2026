# language_python/personal_finance_tracker.py
# S1-P1 – Personal Finance Tracker (Full Sovereign Edition)
# SQLite database + CLI + Matplotlib PDF report

import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === DATABASE SETUP ===
DB_NAME = "finance.db"

def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def create_table():
    """Create the transactions table if it doesn't exist."""
    conn = get_connection()
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
    conn.close()

# === CRUD OPERATIONS ===

def add_transaction(category, amount, date_str, description=""):
    """Insert a new transaction into the database."""
    if amount == 0:
        print("⚠️ Amount cannot be zero. Skipping.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    """, (category, amount, date_str, description))
    conn.commit()
    conn.close()
    print(f"✅ Added: {category} | ₹{amount:,.2f} | {date_str}")

def view_all_transactions():
    """Print all transactions in a readable table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\n📭 No transactions found.")
        return

    print("\n" + "="*70)
    print(f"{'ID':<4} {'Category':<20} {'Amount':>12} {'Date':<12} {'Description'}")
    print("-"*70)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<20} {row[2]:>12,.2f} {row[3]:<12} {row[4]}")
    print("="*70)

def generate_pdf_report():
    """
    Generate a PDF report with:
    1) Bar chart: income vs expense by category
    2) Line chart: cumulative balance over time
    Saves as finance_report_YYYYMMDD.pdf
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount, date FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\n📭 No data to generate report. Add some transactions first.")
        return

    # Prepare data
    categories = {}
    dates = []
    balances = []
    running = 0

    for cat, amt, date_str in rows:
        categories[cat] = categories.get(cat, 0) + amt
        dates.append(date_str)
        running += amt
        balances.append(running)

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # ---- Bar chart: Income vs Expense by Category ----
    cats = list(categories.keys())
    amounts = list(categories.values())
    colors = ['green' if x >= 0 else 'red' for x in amounts]
    ax1.bar(cats, amounts, color=colors, edgecolor='black')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax1.set_title("Income vs Expense by Category", fontsize=14)
    ax1.set_ylabel("Amount (₹)", fontsize=12)
    ax1.set_xlabel("Category", fontsize=12)
    # Add value labels on bars
    for i, v in enumerate(amounts):
        ax1.text(i, v + (100 if v >= 0 else -300), f"₹{v:,.0f}",
                 ha='center', va='bottom' if v >= 0 else 'top', fontsize=9)

    # ---- Line chart: Cumulative Balance ----
    ax2.plot(dates, balances, marker='o', linestyle='-', color='blue', linewidth=2)
    ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax2.set_title("Cumulative Balance Over Time", fontsize=14)
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("Balance (₹)", fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save PDF
    pdf_filename = f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    plt.savefig(pdf_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)  # free memory
    print(f"\n📄 PDF report saved as: {pdf_filename}")
    print(f"   Location: {os.path.abspath(pdf_filename)}")

# === MAIN CLI LOOP ===

def main():
    create_table()  # ensure table exists on startup

    while True:
        print("\n" + "="*50)
        print("  💰 PERSONAL FINANCE TRACKER")
        print("="*50)
        print("  1. Add Income")
        print("  2. Add Expense")
        print("  3. View All Transactions")
        print("  4. Generate PDF Report")
        print("  5. Exit")
        print("-"*50)

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1" or choice == "2":
            try:
                category = input("Category (e.g., Salary, Rent, Food): ").strip()
                if not category:
                    print("❌ Category cannot be empty.")
                    continue

                amount_str = input("Amount (₹): ").strip()
                amount = float(amount_str)
                if amount <= 0:
                    print("❌ Amount must be positive.")
                    continue
                if choice == "2":
                    amount = -amount  # expense → negative

                date_str = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
                if not date_str:
                    date_str = datetime.now().strftime("%Y-%m-%d")

                description = input("Description (optional): ").strip()

                add_transaction(category, amount, date_str, description)

            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == "3":
            view_all_transactions()

        elif choice == "4":
            generate_pdf_report()

        elif choice == "5":
            print("\n👋 Goodbye! Keep building your financial record.")
            break

        else:
            print("❌ Invalid option. Please choose 1-5.")

if __name__ == "__main__":
    main()