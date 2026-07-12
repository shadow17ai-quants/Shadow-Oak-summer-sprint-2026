# 📓 OakLedger – Trading Journal

**Version:** 0.1.0

**Shadow Oak Capitals – S1-P3**

A simple trading journal for logging paper trades, computing performance metrics, and visualising results.

---

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Data Model](#data-model)
- [Testing Instructions](#testing-instructions)
- [Known Limitations](#known-limitations)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

OakLedger provides a CLI for logging trades and a Streamlit dashboard for analysing performance and behavioural patterns. It uses SQLite for persistence and pandas for analysis.

---

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
| **Data Entry** | Log trades with instrument, side, quantity, price, date, reasoning before/after, result, signal used |
| **Data View** | List all trades in CLI or interactive table (web) |
| **Performance Metrics** | Win rate, total P&L, average P&L, max profit/loss, Sharpe ratio |
| **Behavioral Metrics** | Overconfidence, recency bias, loss aversion |
| **Visualization** | Equity curve (line chart) |
| **Persistence** | SQLite database with automatic schema creation |
| **Extensibility** | Easy to add new metrics or fields |

---

## Architecture Overview

```
oakledger/
├─ src/
│  └─ oakledger/
│     ├─ __init__.py
│     ├─ config.py          # Centralized constants and paths
│     ├─ analytics.py       # Performance and behavioural metrics
│     ├─ cli.py             # Command‑line interface
│     └─ dashboard.py       # Streamlit web application
├─ tests/
│  ├─ __init__.py
│  └─ test_analytics.py
├─ trades.db                # SQLite database (auto‑created)
├─ requirements.txt         # Runtime dependencies
└─ README.md                # This file
```

* **Analytics** (`analytics.py`) contains pure functions for computing metrics.
* **CLI** (`cli.py`) provides a text‑menu driven interface for logging and viewing trades.
* **Dashboard** (`dashboard.py`) is a Streamlit app that mirrors the CLI functionality with interactive charts.
* **Config** (`config.py`) holds paths and constants.

---

## Folder Structure

```
oakledger/
├─ src/
│  └─ oakledger/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ analytics.py
│     ├─ cli.py
│     └─ dashboard.py
├─ tests/
│  ├─ __init__.py
│  └─ test_analytics.py
├─ trades.db                # SQLite database (auto‑created)
├─ requirements.txt
└─ README.md
```

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/oakledger.git
   cd oakledger
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
   pip install -e ".[dev]"
   ```

---

## Quick Start

### Launch the CLI

```bash
python -m oakledger.cli
```

Follow the prompts to log trades or view existing ones.

### Launch the Web Dashboard

```bash
streamlit run -m oakledger.dashboard
```

The dashboard opens in your default browser and provides:

* **Dashboard** – key metrics (total trades, win rate, total P&L, Sharpe) and equity curve.
* **All Trades** – searchable, sortable table with all logged trades.
* **Analytics** – behavioural metrics (overconfidence, recency bias, loss aversion).

---

## Usage Examples

### Using the API directly

```python
from oakledger.analytics import load_trades, compute_metrics, behavioral_metrics

df = load_trades()                # loads all trades from the SQLite database
metrics = compute_metrics(df)     # returns a dict with performance stats
behav = behavioral_metrics(df)    # returns a dict with behavioural stats

print(f"Total trades: {metrics['total_trades']}")
print(f"Win rate: {metrics['win_rate']:.2%}")
print(f"Sharpe ratio: {metrics['sharpe_trades']:.2f}")
```

### Running the seed data script (optional)

```bash
python seed-data.py
```

This populates the database with sample trades for demonstration.

---

## Data Model

The `trades` table in SQLite contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto‑incrementing identifier |
| `trade_date` | TEXT (YYYY-MM-DD) | Trade date |
| `instrument` | TEXT | Ticker or instrument name |
| `side` | TEXT | BUY or SELL |
| `quantity` | INTEGER | Number of shares/contracts |
| `price` | REAL | Price per unit |
| `reasoning_before` | TEXT | Notes before entering the trade |
| `reasoning_after` | TEXT | Notes after exiting the trade |
| `result` | REAL | Profit or loss in currency units (positive = profit) |
| `signal_used` | TEXT | Optional label for the strategy/signal that triggered the trade |
| `created_at` | TIMESTAMP | When the record was inserted (default: now) |

All functions in `analytics.py` expect this schema.

---

## Testing Instructions

The project uses **pytest** for unit testing.

```bash
# Install test dependencies (if not already installed)
pip install pytest

# Run the test suite
pytest -v

# To see coverage (optional)
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

### Test Suite Overview

| Test File | Description |
|-----------|-------------|
| `test_analytics.py` | Tests that `load_trades`, `compute_metrics`, and `behavioral_metrics` return expected types and basic correctness. |

All tests should pass on a clean environment.

---

## Known Limitations

| Limitation | Description | Mitigation / Future Work |
|------------|-------------|--------------------------|
| **Single‑user SQLite** | Designed for personal use; concurrent writes from multiple users may cause locks. | Consider migrating to a client‑server DB (e.g., PostgreSQL) for multi‑user scenarios. |
| **No authentication** | Dashboard is accessible to anyone with host/port access. | Deploy behind a reverse proxy with auth, or integrate Streamlit’s authenticator. |
| **Limited visualisation** | Uses Plotly for equity curve only; no interactive filtering in the table. | Add column filters, date range pickers, and more chart types. |
| **No data import/export** | Cannot import existing CSVs or export data for backup. | Future versions could add CSV/JSON import/export features. |
| **Basic behavioural metrics** | Heuristics for overconfidence, recency bias, loss aversion are simplistic. | Refine with more sophisticated models or allow custom metrics. |

---

## Future Roadmap

| Milestone | Goal |
|-----------|------|
| **v1.0.0** | Stabilise core CLI and dashboard, achieve 90 % test coverage, add CI/CD, publish to PyPI. |
| **v1.1.0** | Add data import/export (CSV, JSON). |
| **v1.2.0** | Enhance dashboard with interactive filters and additional charts (e.g., trade frequency histogram). |
| **v1.3.0** | Introduce user authentication and multi‑user support. |
| **v2.0.0** | Provide a Dockerfile and docker‑compose for easy deployment. |
| **v2.1.0** | Add support for multiple portfolios or accounts. |
| **v3.0.0** | Integrate with broker APIs for automatic trade sync. |

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
* **Open‑source community** – Streamlit, Plotly, pandas, SQLite, pytest, Black, Ruff.
* **Beta testers** – teammates who provided early feedback.

---