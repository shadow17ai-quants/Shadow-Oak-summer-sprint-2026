"""
Tests for OakLedger analytics module.
"""

import pandas as pd

from oakledger.analytics import behavioral_metrics, compute_metrics, load_trades


def test_load_trades_returns_dataframe():
    df = load_trades()
    assert isinstance(df, pd.DataFrame)


def test_compute_metrics_returns_dict():
    df = load_trades()
    result = compute_metrics(df)
    assert isinstance(result, dict)
    expected_keys = {
        "total_trades",
        "win_trades",
        "loss_trades",
        "win_rate",
        "loss_rate",
        "total_pnl",
        "avg_pnl",
        "avg_profit",
        "avg_loss",
        "max_profit",
        "max_loss",
        "sharpe_trades",
        "expectancy",
        "rr_ratio",
    }
    assert set(result.keys()) == expected_keys


def test_behavioral_metrics_returns_dict():
    df = load_trades()
    result = behavioral_metrics(df)
    assert isinstance(result, dict)
    expected_keys = {"overconfidence_rate", "recency_bias", "loss_aversion_ratio"}
    assert set(result.keys()) == expected_keys
