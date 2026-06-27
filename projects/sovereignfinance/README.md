# 🏛️ SovereignFinance – Personal Finance Tracker

**Shadow Oak Capitals – S1-P1**

A professional-grade personal finance tracker with CLI and interactive web dashboard. Built with Python, SQLite, Streamlit, and Plotly.

---

## 📌 Features

- 💰 Add income/expense with category, amount, date, description
- 📊 View all transactions with search & filter
- 📈 Interactive charts (bar chart + cumulative balance) using Plotly
- 📄 PDF report generator (CLI only)
- 🖥️ Real‑time web dashboard with Streamlit
- 🛠️ Full CRUD – Add, Edit, Delete transactions
- 🛡️ Input validation and error handling

---

## 🗂️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core language |
| SQLite | Lightweight database |
| Streamlit | Web dashboard |
| Plotly | Interactive charts |
| Matplotlib | PDF report generation |
| Pandas | Data manipulation |

---

## 📦 Installation

```bash
pip install -r requirements.txt
🚀 Usage
CLI (Command Line Interface)
bash
python cli.py
Web Dashboard
bash
streamlit run dashboard.py
📊 Database Schema
sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT
);
🗂️ Project Structure
text
projects/sovereignfinance/
├── cli.py              # Command-line interface
├── dashboard.py        # Streamlit web dashboard
├── finance.db          # SQLite database (auto-created)
├── README.md           # This file
└── requirements.txt    # Python dependencies
🖼️ Dashboard Pages
Page	Description
Summary	Key metrics: Total Income, Total Expense, Net Balance, Transaction Count
All Transactions	Full table with search/filter
Charts	Income/Expense by Category (bar chart) + Cumulative Balance (line chart)
Add Transaction	Form to add new income/expense
Manage	Edit or delete existing transactions
📄 PDF Report
The CLI generates a PDF report with:

Bar chart: Income vs Expense by category

Line chart: Cumulative balance over time

bash
python cli.py
# Select option 4: Generate PDF Report
✅ Mastery Gate (S1-P1)
PDF report with 5+ dummy entries

Bar chart and cumulative balance line chart

README complete

All edge cases handled

Input validation and error handling

CLI + Web Dashboard

Full CRUD (Add, Edit, Delete)

📝 License
This project is part of the Shadow Oak Capitals – 91-Day Summer Sprint and is proprietary.

👤 Author
Ryan Kaushal – Shadow Oak Capitals
Built during the 91-Day Summer Sprint (Sovereign God Edition)

"Nothing you build is practice. Every trade you place is real data. Every paper you publish is permanent capital. Now build."