# MarketVault -- Live Market Dashboard & Strategy Builder

**Version:** 2.0.0
**Shadow Oak Capitals -- S1-P2**

A live Streamlit dashboard pulling real-time data from Yahoo Finance across Indian and global indices, blue-chip NSE stocks, and select US names. Formerly "NifftyVault" (Nifty-50-only) -- renamed and expanded for v2 to reflect broader coverage.

---

## Coverage

**Indices:** Nifty 50, Sensex, Bank Nifty, Nasdaq Composite
**NSE Large-Caps:** Reliance, TCS, Infosys, HDFC Bank, ICICI Bank, Larsen & Toubro, ITC, Bharti Airtel, Axis Bank, Hindustan Unilever
**Other:** ICICI Bank (ADR: IBN), BlackRock (BLK)

## Features

- **Overview** -- price chart with RSI(14) and 20-day annualized volatility overlay
- **Portfolio mode** -- track multiple instruments, normalized growth-of-1 comparison, per-instrument Sharpe/vol/drawdown
- **Top Movers** -- last 10 bars ranked by return
- **Heatmap** -- monthly returns grid
- **Strategy Builder** -- combine Moving Average Crossover, RSI, and Bollinger Band signals with AND/OR logic; backtested equity curve vs buy-and-hold
- **Compare Strategies** -- configure two independent strategies side by side
- **Price alerts** -- sidebar thresholds for RSI overbought/oversold and drawdown severity
- **CSV/report export** -- price data, summary reports, portfolio summaries, strategy backtests

## Run

```powershell
streamlit run src/marketvault/dashboard.py
```

## Theme

Pistachio/sage paper with a maroon accent thread -- deep pistachio for headers, mid pistachio for chart lines, maroon reserved for borders, badges, and sell-side signals.

## Notes

Backtests are signal-only: no transaction costs, slippage, or position sizing. Not investment advice.
