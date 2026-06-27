# language_python/personal_finance_tracker.py
# S1-P1 – Personal Finance Tracker (Day 5: SQLite schema + basic CLI)

import sqlite3
from datetime import date

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# Create table if not exists
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

def add_transaction(category, amount, date_str, description=""):
    cursor.execute("""
    INSERT INTO transactions (category, amount, date, description)
    VALUES (?, ?, ?, ?)
    """, (category, amount, date_str, description))
    conn.commit()
    print(f"✅ Added: {category} | {amount} | {date_str}")

def view_all():
    cursor.execute("SELECT * FROM transactions ORDER BY date")
    rows = cursor.fetchall()
    if not rows:
        print("No transactions found.")
        return
    print("\n===== ALL TRANSACTIONS =====")
    print(f"{'ID':<4} {'Category':<15} {'Amount':<10} {'Date':<12} {'Description'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<15} {row[2]:<10.2f} {row[3]:<12} {row[4]}")
    print("-" * 60)

# Simple CLI loop
def main():
    while True:
        print("\n===== FINANCE TRACKER =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == "1" or choice == "2":
            category = input("Category: ")
            amount = float(input("Amount: "))
            if choice == "2":
                amount = -amount  # expense = negative
            date_str = input("Date (YYYY-MM-DD, leave blank for today): ")
            if not date_str:
                date_str = str(date.today())
            description = input("Description (optional): ")
            add_transaction(category, amount, date_str, description)

        elif choice == "3":
            view_all()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()