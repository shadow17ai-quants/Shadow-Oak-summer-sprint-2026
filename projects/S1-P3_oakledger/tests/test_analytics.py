"""
Tests for OakLedger analytics module.
"""

from oakledger.analytics import load_trades, compute_metrics, behavioral_metrics
import pandas as pd


def test_load_trades_returns_dataframe():
    df = load_trades()
    assert isinstance(df, pd.DataFrame)


def test_compute_metrics_returns_dict():
    df = load_trades()
    result = compute_metrics(df)
    assert isinstance(result, dict)
    expected_keys = {"total_trades", "win_rate", "total_pnl", "avg_pnl", "max_profit", "max_loss", "sharpe_trades"}
    assert set(result.keys()) == expected_keys


def test_behavioral_metrics_returns_dict():
    df = load_trades()
    result = behavioral_metrics(df)
    assert isinstance(result, dict)
    expected_keys = {"overconfidence_rate", "recency_bias", "loss_aversion_ratio"}
    assert set(result.keys()) == expected_keys