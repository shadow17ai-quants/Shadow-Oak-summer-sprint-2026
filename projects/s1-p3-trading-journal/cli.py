# code/s1-p3-trading-journal/cli.py
# S1-P3: Trading Journal – CLI for logging paper trades

import sqlite3
from datetime import datetime

DB_PATH = "code/s1-p3-trading-journal/trades.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    with open("code/s1-p3-trading-journal/schema.sql", "r") as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

def add_trade():
    print("\n=== LOG NEW TRADE ===\n")
    instrument = input("Instrument (e.g., NIFTY 50): ")
    side = input("Side (BUY/SELL): ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))
    reasoning_before = input("Reasoning before trade: ")
    trade_date = input("Date (YYYY-MM-DD, press Enter for today): ") or datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades (trade_date, instrument, side, quantity, price, reasoning_before)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (trade_date, instrument, side, quantity, price, reasoning_before))
    conn.commit()
    conn.close()
    print("✅ Trade logged successfully!")

def view_trades():
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
        print(f"ID: {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | ₹{row[5]:.2f} | {row[6]}")

def main():
    create_table()
    while True:
        print("\n1. Log Trade")
        print("2. View All Trades")
        print("3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_trade()
        elif choice == "2":
            view_trades()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()