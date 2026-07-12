"""
CLI module for OakLedger.
Provides a command-line interface for logging and viewing trades.
"""

import sqlite3
from datetime import datetime

from oakledger.config import DB_PATH


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def create_table():
    """Create the trades table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trade_date TEXT NOT NULL,
            instrument TEXT NOT NULL,
            side TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            reasoning_before TEXT,
            reasoning_after TEXT,
            result REAL,
            signal_used TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_trades_date ON trades(trade_date)")
    conn.commit()
    conn.close()


def add_trade():
    """Prompt the user for trade details and insert a new record."""
    print("\n=== LOG NEW TRADE ===\n")
    instrument = input("Instrument (e.g., NIFTY 50): ").strip()
    side = input("Side (BUY/SELL): ").strip().upper()
    while side not in ("BUY", "SELL"):
        side = input("Please enter BUY or SELL: ").strip().upper()
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))
    reasoning_before = input("Reasoning before trade: ")
    trade_date = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    if not trade_date:
        trade_date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO trades (trade_date, instrument, side, quantity, price, reasoning_before)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (trade_date, instrument, side, quantity, price, reasoning_before),
    )
    conn.commit()
    conn.close()
    print(" Trade logged successfully!")


def view_trades():
    """Fetch and display all trades."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades ORDER BY trade_date DESC")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("No trades logged yet.")
        return
    print("\n=== ALL TRADES ===\n")
    for row in rows:
        print(
            f"ID: {row[0]} | {row[1]} | {row[2]:<10} | {row[3]} | {row[4]} | {row[5]:>8.2f} | {row[6]}"
        )


def main():
    """Main CLI loop."""
    create_table()
    while True:
        print("\n1. Log Trade")
        print("2. View All Trades")
        print("3. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_trade()
        elif choice == "2":
            view_trades()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
