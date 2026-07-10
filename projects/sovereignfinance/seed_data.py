# projects/sovereignfinance/seed_data.py
# One‑time script to fill the database with dummy data for demo

import os
import sqlite3
import random
from datetime import datetime, timedelta

# Allow overriding the database path via environment variable for testing
DB_PATH = os.environ.get("SEED_DB_PATH", "projects/sovereignfinance/finance.db")

# Sample data
categories_income = ["Salary", "Freelance", "Bonus", "Dividend", "Refund"]
categories_expense = ["Rent", "Food", "Transport", "Entertainment", "Utilities"]

def main():
    """Generate and insert dummy transaction data."""
    transactions = []

    # Generate 5 incomes (last 30 days)
    for i in range(5):
        date = (datetime.today() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        cat = random.choice(categories_income)
        amount = random.randint(2000, 60000)
        transactions.append((cat, amount, date, f"Auto {cat} {i+1}"))

    # Generate 10 expenses (last 30 days)
    for i in range(10):
        date = (datetime.today() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        cat = random.choice(categories_expense)
        amount = -random.randint(500, 12000)
        transactions.append((cat, amount, date, f"Auto {cat} {i+1}"))

    # Connect and insert
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create table if not exists (safe)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
        """)

        # Insert all
        cursor.executemany(
            "INSERT INTO transactions (category, amount, date, description) VALUES (?, ?, ?, ?)",
            transactions
        )
        conn.commit()

    print(f"[SUCCESS] Inserted {len(transactions)} dummy transactions into {DB_PATH}")
    print("   Categories: Income (5) + Expense (10)")
    print("   Now run: streamlit run projects/sovereignfinance/dashboard.py")

if __name__ == "__main__":
    main()