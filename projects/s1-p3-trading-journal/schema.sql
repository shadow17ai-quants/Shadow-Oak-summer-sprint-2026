-- S1-P3: Trading Journal – SQLite Schema
-- This journal will later be migrated to PostgreSQL.

CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,                -- ISO date (YYYY-MM-DD)
    instrument TEXT NOT NULL,                -- e.g., "NIFTY 50", "RELIANCE"
    side TEXT NOT NULL,                      -- "BUY" or "SELL"
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    reasoning_before TEXT,                   -- why you placed the trade
    reasoning_after TEXT,                    -- what you learned after
    result REAL,                             -- profit/loss (₹)
    signal_used TEXT,                        -- which signal triggered it
    created_at TEXT DEFAULT (datetime('now'))
);

-- Index for fast querying by date
CREATE INDEX idx_trades_date ON trades(trade_date);