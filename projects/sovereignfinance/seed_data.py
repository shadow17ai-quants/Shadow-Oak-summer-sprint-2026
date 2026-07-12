import os
import random
import sqlite3
from datetime import datetime, timedelta


def main():
    db_path = os.environ.get("SEED_DB_PATH", "projects/sovereignfinance/finance.db")

    categories_income = ["Salary", "Freelance", "Bonus", "Dividend", "Refund"]
    categories_expense = ["Rent", "Food", "Transport", "Entertainment", "Utilities"]

    transactions = []

    for i in range(5):
        date = (datetime.today() - timedelta(days=random.randint(1, 30))).strftime(
            "%Y-%m-%d"
        )
        cat = random.choice(categories_income)
        amount = random.randint(2000, 60000)
        transactions.append((cat, amount, date, f"Auto {cat} {i+1}"))

    for i in range(10):
        date = (datetime.today() - timedelta(days=random.randint(1, 30))).strftime(
            "%Y-%m-%d"
        )
        cat = random.choice(categories_expense)
        amount = -random.randint(500, 12000)
        transactions.append((cat, amount, date, f"Auto {cat} {i+1}"))

    conn = sqlite3.connect(db_path)
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
    cursor.executemany(
        "INSERT INTO transactions (category, amount, date, description) VALUES (?, ?, ?, ?)",
        transactions,
    )
    conn.commit()
    conn.close()

    print(f"Inserted {len(transactions)} dummy transactions into {db_path}")


if __name__ == "__main__":
    main()
