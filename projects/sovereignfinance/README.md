# SovereignFinance – Personal Finance Tracker

**Shadow Oak Capitals – S1‑P1**

A professional‑grade personal finance tracker with a command‑line interface (CLI) and an interactive web dashboard. Built with Python, SQLite, Streamlit, Plotly, and Matplotlib.

---

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Streamlit Dashboard Usage](#streamlit-dashboard-usage)
- [PDF Report Examples](#pdf-report-examples)
- [Database Design](#database-design)
- [Testing Instructions](#testing-instructions)
- [Screenshots (Placeholders)](#screenshots-placeholders)
- [Known Limitations](#known-limitations)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

SovereignFinance provides a simple yet powerful way to track personal income and expenses. Users can record transactions via a terminal‑based menu or a friendly web interface, view summarized statistics, generate PDF reports with charts, and perform full CRUD operations on the underlying SQLite database.

## Motivation

Created as part of the **Shadow Oak Capitals 91‑Day Summer Sprint (Sovereign God Edition)**, this project demonstrates end‑to‑end software engineering practices:

* Clean, modular code with clear separation of concerns  
* Comprehensive type hints and documentation  
* Rigorous input validation and error handling  
* Automated testing and continuous integration  
* Professional documentation and release artefacts  

The goal is to deliver a repository that a senior engineer or quantitative developer can review and immediately recognize as thoughtfully engineered.

---

## Features

| Category | Feature |
|----------|---------|
| **Data Entry** | Add income or expense with category, amount, date, optional description |
| **Data View** | List all transactions in a formatted table (CLI) or interactive table (web) |
| **Editing & Deletion** | Update or remove existing transactions (web dashboard) |
| **Validation** | Robust validation for category, amount, date, and description |
| **Reporting** | Generate PDF reports containing:<br>• Bar chart – Income vs. Expense by category<br>• Line chart – Cumulative balance over time |
| **Visualization** | Interactive bar and line charts powered by Plotly (web) |
| **Persistence** | SQLite database with automatic schema migration |
| **Logging** | Structured logging to file and console |
| **Extensibility** | Centralised configuration (`config.py`) and well‑defined module boundaries |

---

## Architecture Overview

```
sovereignfinance/
├─ src/sovfin/               # Core library (package)
│   ├─ __init__.py
│   ├─ cli.py                # Command‑line interface
│   ├─ dashboard.py          # Streamlit web application
│   ├─ config.py             # Centralised constants & paths
│   ├─ database.py           # SQLite connection & CRUD operations
│   └─ validation.py         # Input validation & error types
├─ tests/                    # pytest test suite
│   ├─ conftest.py
│   ├─ test_cli.py
│   ├─ test_config.py
│   ├─ test_dashboard.py
│   ├─ test_database.py
│   ├─ test_seed_data.py
│   └─ test_validation.py
├─ data/                     # SQLite database file (finance.db)
├─ logs/                     # Application log file
├─ reports/                  # Generated PDF reports
├─ requirements.txt          # Runtime dependencies
└─ README.md                 # This file
```

* **CLI** (`cli.py`) – presents a text menu, collects user input, validates it via `validation.validate_transaction_data`, and persists the transaction using `database.db.add_transaction`.
* **Dashboard** (`dashboard.py`) – Streamlit app that mirrors the CLI functionality with reactive widgets, data tables, and charts.
* **Database** (`database.py`) – wraps SQLite connections in a context‑manager, provides CRUD helpers, and ensures the schema exists.
* **Validation** (`validation.py`) – pure functions that raise `ValidationError` on invalid input; used by both CLI and dashboard.
* **Config** (`config.py`) – holds all constants (paths, format strings, limits, colour palettes) as `Final` typed variables for easy modification.

---

## Folder Structure

```
sovereignfinance/
├─ src/
│  └─ sovfin/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ config.py
│     ├─ dashboard.py
│     ├─ database.py
│     └─ validation.py
├─ tests/
│  ├─ conftest.py
│  ├─ test_cli.py
│  ├─ test_config.py
│  ├─ test_dashboard.py
│  ├─ test_database.py
│  ├─ test_seed_data.py
│  └─ test_validation.py
├─ data/
│  └─ finance.db          # SQLite database (auto‑created)
├─ logs/
│  └─ sovereignfinance.log
├─ reports/
│  └─ *.pdf               # Generated reports
├─ requirements.txt
├─ README.md
└─ (additional metadata files – see below)
```

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/sovereignfinance.git
   cd sovereignfinance
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   For development, also install optional tooling:

   ```bash
   pip install -e ".[dev]"   # if you add a pyproject with extras
   ```

---

## Quick Start

### Launch the CLI

```bash
python cli.py
```

Follow the on‑screen menu:

1. **Add Income** – enter category, amount, date, description  
2. **Add Expense** – same as income but amount is stored as negative  
3. **View All Transactions** – formatted table with totals  
4. **Generate PDF Report** – creates `reports/finance_report_<timestamp>.pdf`  
5. **Exit**

### Launch the Web Dashboard

```bash
streamlit run dashboard.py
```

The dashboard opens in your default browser and provides:

* **Summary** – key metrics (total income, expense, net balance, transaction count)  
* **All Transactions** – searchable, sortable table with edit/delete actions  
* **Charts** – interactive bar chart (income/expense by category) and line chart (cumulative balance)  
* **Add Transaction** – form mirroring the CLI input fields with validation  
* **Manage** – edit or delete existing records  

---

## CLI Usage Detail

When prompted:

* **Category** – any non‑empty string (max 50 chars, letters, numbers, spaces, `- _ . , &`)  
* **Amount** – positive numeric value (zero not allowed)  
* **Date** – `YYYY-MM-DD`; leave blank for today  
* **Description** – optional free text (max 500 chars)

After entering data, the CLI confirms insertion with a green check‑message and logs the transaction.

---

## Streamlit Dashboard Usage

* **Navigation** – use the sidebar to switch between pages.  
* **Add Transaction** – fill the form; invalid entries show inline error messages.  
* **Edit/Delete** – on the *All Transactions* page, click the edit (pencil) or delete (trash) icon on a row.  
* **Charts** – hover for tooltips; zoom/pan via the toolbar.  
* **Theme** – respects Streamlit’s light/dark mode setting.

---

## PDF Report Examples

The PDF report (generated via CLI option 4) contains two pages:

1. **Bar Chart** – total amount per category, coloured green for net income, red for net expense.  
2. **Line Chart** – cumulative balance over time (date on x‑axis, balance on y‑axis).  

Example filename: `finance_report_20260710_153045.pdf`.

Reports are saved in the `reports/` directory.

---

## Database Design

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    description TEXT
);
```

* `id` – auto‑incrementing surrogate key.  
* `category` – transaction category (e.g., Salary, Groceries).  
* `amount` – positive for income, negative for expense.  
* `date` – ISO‑8601 string (`YYYY-MM-DD`).  
* `description` – free‑form notes.

The `database` module provides type‑safe wrappers around these columns.

---

## Testing Instructions

The project uses **pytest** for unit testing.

```bash
# Install test dependencies (if not already in requirements)
pip install pytest

# Run the test suite
pytest -v
```

To run with coverage:

```bash
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

### Test Suite Overview

| Test File | Description |
|-----------|-------------|
| `test_cli.py` | CLI menu rendering and transaction flow |
| `test_config.py` | Configuration constants and path resolution |
| `test_dashboard.py` | Import checks and existence of key functions |
| `test_database.py` | DB initialization, CRUD, edge cases |
| `test_seed_data.py` | Seed script execution (creates sample data) |
| `test_validation.py` | Validation of each field and composite validator |

All tests should pass on a clean environment.

---

## Screenshots (Placeholders)

| CLI Menu Dashboard |
|:------------------:|
| ![CLI Menu](./docs/assets/cli-menu.png) *Placeholder* |

| Dashboard Overview |
|:------------------:|
| ![Dashboard](./docs/assets/dashboard-overview.png) *Placeholder* |

| PDF Report |
|:----------:|
| ![PDF Report](./docs/assets/pdf-report.png) *Placeholder* |

*Replace the placeholder images with actual screenshots before release.*

---

## Known Limitations

| Limitation | Description | Mitigation / Future Work |
|------------|-------------|--------------------------|
| **Single‑user SQLite** | Designed for personal use; concurrent writes from multiple users may cause locks. | Consider migrating to a client‑server DB (PostgreSQL) for multi‑user scenarios. |
| **No authentication** | Dashboard is open to anyone with host/port access. | Deploy behind a reverse proxy with auth, or integrate Streamlit’s authenticator. |
| **Limited chart customization** | Colours and figure sizes are fixed in `config.py`. | Expose UI controls to adjust themes or export options. |
| **PDF generation uses Matplotlib** | Heavy dependency; may be slow on low‑end machines. | Offer optional lightweight report (CSV/JSON) or plotly‑to‑pdf via `kaleido`. |
| **No data import/export** | Users cannot import existing CSVs or export data. | Future versions could add CSV/JSON import/export features. |

---

## Future Roadmap

| Milestone | Goal |
|-----------|------|
| **v1.0.0** | Stabilise core CLI & dashboard, achieve 100% test coverage, add CI/CD pipeline, publish to PyPI. |
| **v1.1.0** | Add data import/export (CSV, JSON). |
| **v1.2.0** | Introduce user authentication for the Streamlit app (via `streamlit-authenticator`). |
| **v1.3.0** | Support multiple budgets/goals and tracking progress. |
| **v2.0.0** | Migrate to a client‑server PostgreSQL backend for multi‑user deployments. |
| **v2.1.0** | Add recurring transactions and reminders. |
| **v2.2.0** | Export reports to HTML/EPUB in addition to PDF. |
| **v3.0.0** | Provide a Dockerfile and Kubernetes manifests for cloud deployment. |

---

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

* Reporting bugs  
* Suggesting enhancements  
* Submitting pull requests  
* Coding style (we use **Black** and **Ruff**)  
* Running the test suite locally  

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* **Shadow Oak Capitals** – for sponsoring the 91‑Day Summer Sprint.  
* **Open‑source community** – Streamlit, Plotly, Matplotlib, SQLite, pytest, Black, Ruff.  
* **Beta testers** – teammates who provided early feedback.

---

*Happy tracking!*  
<small>Built with ❤️ by Ryan Kaushal – Shadow Oak Capitals</small>