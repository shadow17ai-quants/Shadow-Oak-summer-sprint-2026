"""
Seed OakLedger with realistic dummy trades for dashboard testing.
"""
import sqlite3
import random
from datetime import datetime, timedelta
from oakledger.config import DB_PATH

random.seed(42)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS trades (
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
)""")
c.execute("DELETE FROM trades")

instruments = ["NIFTY 50", "RELIANCE", "HDFC BANK", "INFY", "TCS", "ICICI BANK", "SBIN", "AXIS BANK"]
sides = ["BUY", "SELL"]
signals = ["Momentum", "MeanRev", "Carry", "Breakout"]
reasons_long = [
    "Strong breakout above resistance with volume confirmation and RSI divergence supporting continuation",
    "Mean reversion setup after extended move, price at 2 std dev from 20-day moving average",
    "Trend-following entry on pullback to 50 EMA within established uptrend structure",
]
reasons_short = ["Gut feel", "FOMO", "Tip"]

trades = []
n_trades = 93  # matches "52 win / 41 loss" style reference
start_date = datetime.today() - timedelta(days=150)

for i in range(n_trades):
    trade_date = (start_date + timedelta(days=random.randint(0, 150))).strftime("%Y-%m-%d")
    instrument = random.choice(instruments)
    side = random.choice(sides)
    quantity = random.randint(1, 10)
    price = round(random.uniform(100, 5000), 2)
    signal = random.choice(signals)

    # ~56% win rate, winners skew smaller than losers occasionally to make Sharpe/expectancy interesting
    is_win = random.random() < 0.56
    if is_win:
        result = round(random.uniform(500, 8000), 2)
        reasoning_before = random.choice(reasons_long)
    else:
        result = round(-random.uniform(300, 6000), 2)
        reasoning_before = random.choice(reasons_long + reasons_short)

    reasoning_after = "Target hit, closed per plan" if is_win else "Stopped out, reviewed setup"
    trades.append((trade_date, instrument, side, quantity, price, reasoning_before, reasoning_after, result, signal))

trades.sort(key=lambda t: t[0])

c.executemany(
    """INSERT INTO trades (trade_date, instrument, side, quantity, price, reasoning_before, reasoning_after, result, signal_used)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    trades,
)
conn.commit()
conn.close()
print(f"Inserted {len(trades)} trades into {DB_PATH}")