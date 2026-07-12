"""
quant_stats - Financial Statistics Library v0.1
Shadow Oak Capitals - S1-P4 sprint deliverable.
"""

from quant_stats.ratios import (
    sharpe_ratio,
    sortino_ratio,
    calmar_ratio,
    omega_ratio,
    max_drawdown,
)
from quant_stats.hypothesis_tests import (
    jarque_bera_test,
    shapiro_wilk_test,
    ljung_box_test,
    adf_test,
    fit_student_t,
)

__all__ = [
    "sharpe_ratio",
    "sortino_ratio",
    "calmar_ratio",
    "omega_ratio",
    "max_drawdown",
    "jarque_bera_test",
    "shapiro_wilk_test",
    "ljung_box_test",
    "adf_test",
    "fit_student_t",
]


def full_report(returns, periods_per_year=252):
    """Run all 10 functions on a return series and return one combined dict."""
    return {
        "sharpe_ratio": sharpe_ratio(returns, periods_per_year=periods_per_year),
        "sortino_ratio": sortino_ratio(returns, periods_per_year=periods_per_year),
        "calmar_ratio": calmar_ratio(returns, periods_per_year=periods_per_year),
        "omega_ratio": omega_ratio(returns),
        "max_drawdown": max_drawdown(returns),
        "jarque_bera_test": jarque_bera_test(returns),
        "shapiro_wilk_test": shapiro_wilk_test(returns),
        "ljung_box_test": ljung_box_test(returns),
        "adf_test": adf_test(returns),
        "fit_student_t": fit_student_t(returns),
    }
