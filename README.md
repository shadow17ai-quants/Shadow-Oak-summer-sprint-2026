# Shadow Oak Summer Sprint 2026

**91‑day institutional‑grade quant research sprint**

This repository contains all code, projects, papers, and journals for the **Shadow Oak Capitals – Summer Sprint 2026** – a systematic quantitative hedge fund incubator.

---

## 📌 Overview

- **Duration:** 19 June – 17 September 2026 (91 days)
- **Goal:** Build a complete quant research platform with 21 projects, 3 SSRN papers, and a live‑trading infrastructure.
- **Edge, Proof, Trust, Capital** – all four pillars must be satisfied before fund launch.

---

## 🗂️ Repository Structure
├── code/ # All project code (organized by deliverable)
├── daily_log/ # Daily logs (Day 1 – Day 91)
├── journals/ # Sunday journals (Week 1 – Week 13)
├── docs/ # Finance and statistics notes
├── papers/ # SSRN paper drafts and final PDFs
├── projects/ # Completed projects (SovereignFinance, NifftyVault, etc.)
├── language_python/ # Learning scripts (Mosh, Corey, etc.)
└── README.md # This file

text

---

## 📊 Completed Projects

| Project | Folder | Status |
|---------|--------|--------|
| **SovereignFinance** – Personal Finance Tracker (CLI + Web Dashboard) | `projects/sovereignfinance/` | ✅ |
| **NifftyVault** – Nifty 50 Data Downloader & Analyzer (Sharpe, drawdown) | `projects/nifftyvault/` | ✅ |

---

## 🔧 Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (for later phases)
- Git

### Installation

```bash
pip install -r requirements.txt
Run a Project
bash
cd projects/sovereignfinance
python cli.py
Or launch the web dashboard:

bash
streamlit run projects/sovereignfinance/dashboard.py
📈 Phase 1 Deliverables (July 4, 2026)
Deliverable	Status
Python fundamentals (Mosh Ep 1–12 + Corey OOP 1–4)	✅
Git setup with 20+ commits	✅
S1‑P1: Personal Finance Tracker (SQLite + PDF)	✅
S1‑P2: Nifty 50 Data Downloader (Sharpe + drawdown)	✅
Week 2 Sunday Journal	✅
Paper 1 (SSRN submission)	🔴 In progress
📝 License
Proprietary – part of Shadow Oak Capitals Summer Sprint.

Built by Ryan Kaushal – Shadow Oak Capitals
"Nothing you build is practice."

text

---

## 📁 Step 4: Create Finance Notes

### File: `docs/finance_notes.md`

```markdown
# Finance Notes – Sharpe, Sortino, Calmar

## Sharpe Ratio

**Formula:**

$$ \text{Sharpe} = \frac{R_p - R_f}{\sigma_p} $$

- \( R_p \) = Portfolio return (annualised)
- \( R_f \) = Risk‑free rate (often 0 for this sprint)
- \( \sigma_p \) = Portfolio volatility (annualised)

**Interpretation:**
- Higher = better risk‑adjusted return.
- A Sharpe > 1 is considered good.
- Our Nifty 50 data showed Sharpe ≈ 0.73 (annualised, zero risk‑free).

---

## Sortino Ratio

**Formula:**

$$ \text{Sortino} = \frac{R_p - R_f}{\sigma_d} $$

- \( \sigma_d \) = Downside deviation (only negative returns)

**Interpretation:**
- Focuses on downside risk only, ignores upside volatility.
- More relevant for asymmetric return distributions.

---

## Calmar Ratio

**Formula:**

$$ \text{Calmar} = \frac{R_p}{\text{Max Drawdown}} $$

- Max Drawdown = peak‑to‑trough decline

**Interpretation:**
- Higher is better.
- Used to compare strategies based on worst‑case loss.

---

## Annualisation

- **Trading days per year:** 252 (used for equities)
- **Annualised Return:** \( (1 + R_d)^{252} - 1 \)
- **Annualised Volatility:** \( \sigma_d \times \sqrt{252} \)

