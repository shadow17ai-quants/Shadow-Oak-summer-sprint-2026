import numpy as np
from quant_stats.ratios import (
    sharpe_ratio, sortino_ratio, calmar_ratio, omega_ratio, max_drawdown,
)


def test_sharpe_ratio_constant_positive(constant_positive_returns):
    result = sharpe_ratio(constant_positive_returns)
    expected_ann_return = (1.001) ** 252 - 1
    assert np.isclose(result["annualized_return"], expected_ann_return, rtol=1e-6)
    assert np.isclose(result["annualized_volatility"], 0.0, atol=1e-9)
    assert result["sharpe_ratio"] == np.inf


def test_sharpe_ratio_zero_returns(zero_returns):
    result = sharpe_ratio(zero_returns)
    assert result["annualized_return"] == 0.0
    assert result["sharpe_ratio"] == 0.0


def test_sortino_ratio_no_downside(constant_positive_returns):
    result = sortino_ratio(constant_positive_returns)
    assert result["downside_deviation"] == 0.0
    assert result["sortino_ratio"] == np.inf


def test_max_drawdown_known_sequence(known_drawdown_returns):
    result = max_drawdown(known_drawdown_returns)
    # cumulative: 1.10, 0.88, 0.924 -> peak 1.10 at idx0, trough 0.88 at idx1
    expected_dd = (0.88 - 1.10) / 1.10
    assert np.isclose(result["max_drawdown"], expected_dd, rtol=1e-6)
    assert result["peak_index"] == 0
    assert result["trough_index"] == 1


def test_max_drawdown_all_positive():
    result = max_drawdown(np.array([0.01, 0.02, 0.01, 0.03]))
    assert np.isclose(result["max_drawdown"], 0.0)


def test_calmar_ratio_known_sequence(known_drawdown_returns):
    result = calmar_ratio(known_drawdown_returns, periods_per_year=252)
    mean_daily = known_drawdown_returns.mean()
    expected_ann_return = (1 + mean_daily) ** 252 - 1
    assert np.isclose(result["annualized_return"], expected_ann_return, rtol=1e-6)
    assert result["calmar_ratio"] == expected_ann_return / abs(result["max_drawdown"])


def test_omega_ratio_all_gains(constant_positive_returns):
    result = omega_ratio(constant_positive_returns, threshold=0.0)
    assert result["losses_sum"] == 0.0
    assert result["omega_ratio"] == np.inf


def test_omega_ratio_mixed():
    r = np.array([0.02, -0.01, 0.03, -0.02])
    result = omega_ratio(r, threshold=0.0)
    assert np.isclose(result["gains_sum"], 0.05)
    assert np.isclose(result["losses_sum"], 0.03)
    assert np.isclose(result["omega_ratio"], 0.05 / 0.03)


def test_empty_input_all_functions():
    empty = np.array([])
    assert np.isnan(sharpe_ratio(empty)["sharpe_ratio"])
    assert np.isnan(sortino_ratio(empty)["sortino_ratio"])
    assert np.isnan(calmar_ratio(empty)["calmar_ratio"])
    assert np.isnan(omega_ratio(empty)["omega_ratio"])
    assert np.isnan(max_drawdown(empty)["max_drawdown"])
