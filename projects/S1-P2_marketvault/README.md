MarketVault — Live Market Dashboard & Strategy Builder
​Version: 2.0.0 | Project: Shadow Oak Capitals (S1-P2)
​MarketVault (formerly NifftyVault) is a real-time Streamlit dashboard that aggregates market data via Yahoo Finance. It provides live tracking, portfolio benchmarking, and a custom rule-based backtesting engine across Indian and global indices, NSE large-caps, and select US equities.
​📊 Market Coverage
​Indices: Nifty 50, Sensex, Bank Nifty, Nasdaq Composite
​NSE Large-Caps: Reliance, TCS, Infosys, HDFC Bank, ICICI Bank, L&T, ITC, Bharti Airtel, Axis Bank, HUL
​US Equities & ADRs: BlackRock (BLK), ICICI Bank ADR (IBN)
​✨ Features
​Live Overview: Interactive price charts overlaid with RSI(14) and 20-day annualized volatility.
​Portfolio Mode: Multi-instrument tracking with normalized growth-of-$1 comparisons and key risk metrics (Sharpe ratio, volatility, max drawdown).
​Top Movers: Real-time ranking of the top 10 instruments by return over the last 10 bars.
​Monthly Heatmap: A visual grid mapping historical monthly returns.
​Strategy Builder: Code-free backtesting. Combine Moving Average Crossovers, RSI, and Bollinger Bands using customizable AND / OR logic to compare equity curves against Buy-and-Hold.
​Strategy Comparison: Configure and benchmark two independent strategies side-by-side.
​Smart Alerts: Sidebar thresholds for RSI overbought/oversold levels and drawdown severity.
​Data Export: One-click CSV/Report generation for price data, summary metrics, portfolio performance, and backtest results.
​🎨 UI Theme
​The dashboard features a curated Pistachio & Maroon aesthetic:
​Headers: Deep Pistachio
​Chart Lines: Mid Pistachio
​Borders, Badges & Sell Signals: Maroon accent threading
​🚀 Quick Start
​Launch the Streamlit dashboard locally via PowerShell or your terminal:

streamlit run src/marketvault/dashboard.py


⚠️ Disclaimer
Backtest Constraints: Performance simulations are signal-only. They do not account for transaction costs, slippage, taxes, or advanced position sizing.
Not Financial Advice: This software is for educational and analytical purposes only.