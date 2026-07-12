# S1-P1: Sovereign Personal Finance Ingestion and Diagnostic Architecture
"""
Compiles financial tracker modules leveraging SQLite infrastructure alongside structured
Matplotlib PDF generators mapping comprehensive operational assets from Day 1.
"""
import sqlite3
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

DATABASE_PATH = "personal_finances.db"

def initialize_database() -> None:
    """Establishes internal database layout mapping transaction ledgers securely."""
    with sqlite3.connect(DATABASE_PATH) as database_connection:
        cursor = database_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaction_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('INCOME', 'EXPENSE')),
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0.0)
            );
        """)
        database_connection.commit()

def register_transaction(date_str: str, entry_type: str, category_str: str, total_volume: float) -> None:
    """Commits analytical entries safely into the transaction database."""
    # Ensure correct format structure validation
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Data Mismatch: Date parameter '{date_str}' must strictly align with %Y-%m-%d.")
        return

    with sqlite3.connect(DATABASE_PATH) as database_connection:
        cursor = database_connection.cursor()
        cursor.execute("""
            INSERT INTO transaction_ledger (date, type, category, amount)
            VALUES (?, ?, ?, ?);
        """, (date_str, entry_type.upper(), category_str.strip().upper(), total_volume))
        database_connection.commit()
    print(f"Success: Registered {entry_type} entry for category '{category_str}' [Amount: {total_volume}].")

def extract_and_serialize_pdf_report(start_date: str, end_date: str, target_pdf_name: str = "Finance_Tracker_Audit.pdf") -> None:
    """
    Extracts isolated ledger slices, computes metric aggregations, and prints highly formatted 
    analytical sheets. Handles empty ranges cleanly without cracking.
    """
    with sqlite3.connect(DATABASE_PATH) as database_connection:
        database_connection.row_factory = sqlite3.Row
        cursor = database_connection.cursor()
        cursor.execute("""
            SELECT * FROM transaction_ledger 
            WHERE date BETWEEN ? AND ? 
            ORDER BY date ASC;
        """, (start_date, end_date))
        matching_rows = cursor.fetchall()

    if not matching_rows:
        print(f"System Log Alert: No data in this range '{start_date}' to '{end_date}'. Aborting compilation.")
        return

    # Aggregate computational tracking categories
    category_map = {}
    net_timeline_balance = 0.0
    timeline_dates = []
    cumulative_balances = []

    for row in matching_rows:
        amount = row["amount"]
        category = row["category"]
        entry_type = row["type"]
        date_obj = datetime.strptime(row["date"], "%Y-%m-%d")

        multiplier = 1.0 if entry_type == "INCOME" else -1.0
        net_timeline_balance += (amount * multiplier)

        timeline_dates.append(date_obj)
        cumulative_balances.append(net_timeline_balance)

        if entry_type == "EXPENSE":
            category_map[category] = category_map.get(category, 0.0) + amount

    # Generate analytical graphic sheets via context layout configurations
    fig, (ax_bar, ax_line) = plt.subplots(2, 1, figsize=(10, 12))
    
    # Render expense breakout mapping parameters
    if category_map:
        categories = list(category_map.keys())
        expenditures = list(category_map.values())
        ax_bar.bar(categories, expenditures, color="#E63946", edgecolor="black")
        ax_bar.set_title("Categorical Expense Breakdown Metrics")
        ax_bar.set_ylabel("Capital Volume (INR)")
    else:
        ax_bar.text(0.5, 0.5, "Zero Expense Entries Registered in Timeline Slice", ha='center', va='center')

    # Render continuous asset timeline configurations
    ax_line.plot(timeline_dates, cumulative_balances, color="#1D3557", marker='o', linewidth=2)
    ax_line.set_title("Cumulative Operational Balance Scaling Progression")
    ax_line.set_xlabel("Timeline Coordination Intercepts")
    ax_line.set_ylabel("Net Liquidity Level (INR)")
    ax_line.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    
    with PdfPages(target_pdf_name) as target_pdf_document:
        target_pdf_document.savefig(fig)
    plt.close()
    print(f"Success: Compiled comprehensive analytical framework sheet directly to file path: {target_pdf_name}")

if __name__ == "__main__":
    initialize_database()
    # Seeding minimum 5 operational dummy lines to satisfy done-when requirements safely
    register_transaction("2026-06-20", "INCOME", "Allocation Base", 20000.0)
    register_transaction("2026-06-22", "EXPENSE", "Compute Node", 1200.50)
    register_transaction("2026-06-25", "EXPENSE", "Connectivity", 450.00)
    register_transaction("2026-07-01", "INCOME", "Yield Inflow", 3500.00)
    register_transaction("2026-07-10", "EXPENSE", "Infrastructure Books", 650.00)
    
    # Run structural compile runs
    extract_and_serialize_pdf_report("2026-06-19", "2026-07-13")
