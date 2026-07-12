"""
Financial Statistics Library v0.1 - Ratio and Drawdown Functions
Shadow Oak Capitals - S1-P4
"""
import numpy as np


def _clean(returns):
    arr = np.asarray(returns, dtype=float)
    return arr[~np.isnan(arr)]


def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
    r = _clean(returns)
    if len(r) == 0:
        return {"sharpe_ratio": np.nan, "annualized_return": np.nan, "annualized_volatility": np.nan}
    mean_daily = r.mean()
    std_daily = r.std(ddof=1) if len(r) > 1 else 0.0
    ann_return = (1 + mean_daily) ** periods_per_year - 1
    ann_vol = std_daily * np.sqrt(periods_per_year)
    if ann_vol < 1e-12:
        sharpe = np.inf if ann_return > risk_free_rate else (0.0 if ann_return == risk_free_rate else -np.inf)
    else:
        sharpe = (ann_return - risk_free_rate) / ann_vol
    return {"sharpe_ratio": sharpe, "annualized_return": ann_return, "annualized_volatility": ann_vol}


def sortino_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
    r = _clean(returns)
    if len(r) == 0:
        return {"sortino_ratio": np.nan, "annualized_return": np.nan, "downside_deviation": np.nan}
    mean_daily = r.mean()
    ann_return = (1 + mean_daily) ** periods_per_year - 1
    downside = r[r < 0]
    downside_dev = np.sqrt(np.mean(downside ** 2)) * np.sqrt(periods_per_year) if len(downside) > 0 else 0.0
    if downside_dev < 1e-12:
        sortino = np.inf if ann_return > risk_free_rate else (0.0 if ann_return == risk_free_rate else -np.inf)
    else:
        sortino = (ann_return - risk_free_rate) / downside_dev
    return {"sortino_ratio": sortino, "annualized_return": ann_return, "downside_deviation": downside_dev}


def max_drawdown(returns):
    r = _clean(returns)
    if len(r) == 0:
        return {"max_drawdown": np.nan, "peak_index": None, "trough_index": None}
    cumulative = np.cumprod(1 + r)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    trough_idx = int(np.argmin(drawdown))
    peak_idx = int(np.argmax(cumulative[: trough_idx + 1])) if trough_idx > 0 else 0
    return {"max_drawdown": float(drawdown[trough_idx]), "peak_index": peak_idx, "trough_index": trough_idx}


def calmar_ratio(returns, periods_per_year=252):
    r = _clean(returns)
    if len(r) == 0:
        return {"calmar_ratio": np.nan, "annualized_return": np.nan, "max_drawdown": np.nan}
    mean_daily = r.mean()
    ann_return = (1 + mean_daily) ** periods_per_year - 1
    mdd_result = max_drawdown(r)
    mdd = abs(mdd_result["max_drawdown"])
    if mdd < 1e-12:
        calmar = np.inf if ann_return > 0 else (0.0 if ann_return == 0 else -np.inf)
    else:
        calmar = ann_return / mdd
    return {"calmar_ratio": calmar, "annualized_return": ann_return, "max_drawdown": mdd_result["max_drawdown"]}


def omega_ratio(returns, threshold=0.0):
    r = _clean(returns)
    if len(r) == 0:
        return {"omega_ratio": np.nan, "gains_sum": np.nan, "losses_sum": np.nan}
    excess = r - threshold
    gains = excess[excess > 0].sum()
    losses = -excess[excess < 0].sum()
    omega = np.inf if losses == 0 and gains > 0 else (np.nan if losses == 0 else gains / losses)
    return {"omega_ratio": omega, "gains_sum": float(gains), "losses_sum": float(losses)}
