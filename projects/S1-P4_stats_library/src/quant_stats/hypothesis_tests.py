"""
Financial Statistics Library v0.1 - Statistical Hypothesis Tests
Shadow Oak Capitals - S1-P4
"""

import warnings
import numpy as np
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller


def _clean(returns):
    arr = np.asarray(returns, dtype=float)
    return arr[~np.isnan(arr)]


def jarque_bera_test(returns):
    r = _clean(returns)
    if len(r) < 2:
        return {
            "statistic": np.nan,
            "p_value": np.nan,
            "interpretation": "insufficient data",
        }
    stat, p_value = stats.jarque_bera(r)
    interp = (
        "NOT normally distributed (reject H0)"
        if p_value < 0.05
        else "cannot reject normality (fail to reject H0)"
    )
    return {
        "statistic": float(stat),
        "p_value": float(p_value),
        "interpretation": interp,
    }


def shapiro_wilk_test(returns):
    r = _clean(returns)
    if len(r) < 3:
        return {
            "statistic": np.nan,
            "p_value": np.nan,
            "interpretation": "insufficient data",
        }
    if len(r) > 5000:
        r = r[:5000]
    stat, p_value = stats.shapiro(r)
    interp = (
        "NOT normally distributed (reject H0)"
        if p_value < 0.05
        else "cannot reject normality (fail to reject H0)"
    )
    return {
        "statistic": float(stat),
        "p_value": float(p_value),
        "interpretation": interp,
    }


def ljung_box_test(returns, lags=10):
    r = _clean(returns)
    if len(r) < lags + 1:
        return {
            "statistic": np.nan,
            "p_value": np.nan,
            "interpretation": "insufficient data",
        }
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = acorr_ljungbox(r, lags=[lags], return_df=True)
    stat = float(result["lb_stat"].iloc[0])
    p_value = float(result["lb_pvalue"].iloc[0])
    interp = (
        "significant autocorrelation (reject H0)"
        if p_value < 0.05
        else "no significant autocorrelation (fail to reject H0)"
    )
    return {"statistic": stat, "p_value": p_value, "interpretation": interp}


def adf_test(returns):
    r = _clean(returns)
    if len(r) < 5:
        return {
            "statistic": np.nan,
            "p_value": np.nan,
            "interpretation": "insufficient data",
        }
    result = adfuller(r, autolag="AIC")
    stat, p_value = result[0], result[1]
    interp = (
        "stationary (reject H0 of unit root)"
        if p_value < 0.05
        else "NOT stationary (fail to reject H0 of unit root)"
    )
    return {
        "statistic": float(stat),
        "p_value": float(p_value),
        "interpretation": interp,
    }


def fit_student_t(returns):
    r = _clean(returns)
    if len(r) < 5:
        return {
            "statistic": np.nan,
            "p_value": np.nan,
            "degrees_of_freedom": np.nan,
            "interpretation": "insufficient data",
        }
    df, loc, scale = stats.t.fit(r)
    ks_stat, ks_p = stats.kstest(r, "t", args=(df, loc, scale))
    if df < 5:
        interp = f"extreme fat tails (df={df:.2f} < 5)"
    elif df <= 10:
        interp = f"moderate fat tails (5 <= df={df:.2f} <= 10)"
    else:
        interp = f"near-normal tails (df={df:.2f} > 10)"
    return {
        "statistic": float(ks_stat),
        "p_value": float(ks_p),
        "degrees_of_freedom": float(df),
        "loc": float(loc),
        "scale": float(scale),
        "interpretation": interp,
    }
