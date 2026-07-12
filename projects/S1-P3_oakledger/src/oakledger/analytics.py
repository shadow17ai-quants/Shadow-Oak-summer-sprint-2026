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
    if df.empty or 'result' not in df.columns:
        return {"total_trades": 0, "win_rate": 0.0, "total_pnl": 0.0, "avg_pnl": 0.0, "max_profit": 0.0, "max_loss": 0.0, "sharpe_trades": 0.0}
    # Use 'result' column for P&L
    df = df.copy()
    df['result'] = pd.to_numeric(df['result'], errors='coerce')
    clean = df[df['result'].notna()]
    if clean.empty:
        return {"total_trades": len(df), "win_rate": 0.0, "total_pnl": 0.0, "avg_pnl": 0.0, "max_profit": 0.0, "max_loss": 0.0, "sharpe_trades": 0.0}
    wins = clean[clean['result'] > 0]
    mean_pnl = clean['result'].mean()
    std_pnl = clean['result'].std()
    return {
        "total_trades": len(clean),
        "win_rate": len(wins) / len(clean) if len(clean) > 0 else 0.0,
        "total_pnl": clean['result'].sum(),
        "avg_pnl": mean_pnl,
        "max_profit": clean['result'].max(),
        "max_loss": clean['result'].min(),
        "sharpe_trades": mean_pnl / std_pnl if std_pnl > 0 else 0.0
    }


def behavioral_metrics(df: pd.DataFrame) -> dict:
    """Compute behavioural metrics from trades DataFrame."""
    if df.empty or 'result' not in df.columns:
        return {"overconfidence_rate": 0.0, "recency_bias": 0.0, "loss_aversion_ratio": 0.0}
    df = df.copy()
    df['result'] = pd.to_numeric(df['result'], errors='coerce')
    clean = df[df['result'].notna()]
    if clean.empty:
        return {"overconfidence_rate": 0.0, "recency_bias": 0.0, "loss_aversion_ratio": 0.0}
    # Overconfidence: short reasoning (<20 chars) that lost
    if 'reasoning_before' in clean.columns:
        short = clean[clean['reasoning_before'].fillna('').str.len() < 20]
        over = len(short[short['result'] < 0]) / len(short) if len(short) > 0 else 0.0
    else:
        over = 0.0
    # Recency bias: compare win rate of last 5 trades to overall
    last5 = clean.tail(5)
    recent_win = (last5['result'] > 0).mean() if len(last5) > 0 else 0.0
    overall_win = (clean['result'] > 0).mean() if len(clean) > 0 else 0.0
    recency = recent_win - overall_win
    # Loss aversion ratio: #losers / #winners
    winners = clean[clean['result'] > 0]
    losers = clean[clean['result'] < 0]
    loss_aversion = len(losers) / len(winners) if len(winners) > 0 else 0.0
    return {"overconfidence_rate": over, "recess_bias": recency, "loss_aversion_ratio": loss_aversion}