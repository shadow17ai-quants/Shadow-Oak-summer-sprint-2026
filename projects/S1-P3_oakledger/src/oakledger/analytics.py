"""
Analytics module for OakLedger.
Contains functions for loading trade data and computing metrics.
"""

import sqlite3

import pandas as pd

from oakledger.config import DB_PATH


def load_trades() -> pd.DataFrame:
    """Load all trades from the SQLite database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("SELECT * FROM trades", conn)
    except Exception:
        df = pd.DataFrame()
    return df


def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute performance metrics from trades DataFrame."""
    empty = {
        "total_trades": 0,
        "win_trades": 0,
        "loss_trades": 0,
        "win_rate": 0.0,
        "loss_rate": 0.0,
        "total_pnl": 0.0,
        "avg_pnl": 0.0,
        "avg_profit": 0.0,
        "avg_loss": 0.0,
        "max_profit": 0.0,
        "max_loss": 0.0,
        "sharpe_trades": 0.0,
        "expectancy": 0.0,
        "rr_ratio": 0.0,
    }
    if df.empty or "result" not in df.columns:
        return empty

    df = df.copy()
    df["result"] = pd.to_numeric(df["result"], errors="coerce")
    clean = df[df["result"].notna()]
    if clean.empty:
        empty["total_trades"] = len(df)
        return empty

    wins = clean[clean["result"] > 0]
    losses = clean[clean["result"] < 0]
    mean_pnl = clean["result"].mean()
    std_pnl = clean["result"].std()
    avg_profit = wins["result"].mean() if len(wins) > 0 else 0.0
    avg_loss = losses["result"].mean() if len(losses) > 0 else 0.0
    win_rate = len(wins) / len(clean) if len(clean) > 0 else 0.0
    loss_rate = len(losses) / len(clean) if len(clean) > 0 else 0.0
    expectancy = (win_rate * avg_profit) + (loss_rate * avg_loss)
    rr_ratio = abs(avg_profit / avg_loss) if avg_loss != 0 else 0.0

    return {
        "total_trades": len(clean),
        "win_trades": len(wins),
        "loss_trades": len(losses),
        "win_rate": win_rate,
        "loss_rate": loss_rate,
        "total_pnl": clean["result"].sum(),
        "avg_pnl": mean_pnl,
        "avg_profit": avg_profit,
        "avg_loss": avg_loss,
        "max_profit": clean["result"].max(),
        "max_loss": clean["result"].min(),
        "sharpe_trades": mean_pnl / std_pnl if std_pnl > 0 else 0.0,
        "expectancy": expectancy,
        "rr_ratio": rr_ratio,
    }


def behavioral_metrics(df: pd.DataFrame) -> dict:
    """Compute behavioural metrics from trades DataFrame."""
    empty = {
        "overconfidence_rate": 0.0,
        "recency_bias": 0.0,
        "loss_aversion_ratio": 0.0,
    }
    if df.empty or "result" not in df.columns:
        return empty
    df = df.copy()
    df["result"] = pd.to_numeric(df["result"], errors="coerce")
    clean = df[df["result"].notna()]
    if clean.empty:
        return empty

    if "reasoning_before" in clean.columns:
        short = clean[clean["reasoning_before"].fillna("").str.len() < 20]
        over = len(short[short["result"] < 0]) / len(short) if len(short) > 0 else 0.0
    else:
        over = 0.0

    last5 = clean.tail(5)
    recent_win = (last5["result"] > 0).mean() if len(last5) > 0 else 0.0
    overall_win = (clean["result"] > 0).mean() if len(clean) > 0 else 0.0
    recency = recent_win - overall_win

    winners = clean[clean["result"] > 0]
    losers = clean[clean["result"] < 0]
    loss_aversion = len(losers) / len(winners) if len(winners) > 0 else 0.0

    return {
        "overconfidence_rate": over,
        "recency_bias": recency,
        "loss_aversion_ratio": loss_aversion,
    }


def monthly_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate P&L by month for bar charts."""
    if df.empty or "result" not in df.columns or "trade_date" not in df.columns:
        return pd.DataFrame(columns=["month", "pnl"])
    d = df.copy()
    d["result"] = pd.to_numeric(d["result"], errors="coerce")
    d["trade_date"] = pd.to_datetime(d["trade_date"], errors="coerce")
    d = d.dropna(subset=["result", "trade_date"])
    if d.empty:
        return pd.DataFrame(columns=["month", "pnl"])
    d["month"] = d["trade_date"].dt.to_period("M").astype(str)
    return (
        d.groupby("month", as_index=False)["result"]
        .sum()
        .rename(columns={"result": "pnl"})
    )
