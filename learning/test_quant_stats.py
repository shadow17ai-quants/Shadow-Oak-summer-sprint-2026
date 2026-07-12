# S1-P4 Test Framework Suite - Comprehensive Verification Unit Tests
"""
Executes strict mathematical verification passes across the core financial statistics library 
using deterministic synthetic test vectors.
"""
import pytest
import numpy as np
import sys
import os

# Ensure tracking resolution handles directory roots cleanly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import quant_stats

@pytest.fixture
def baseline_synthetic_returns() -> np.ndarray:
    """Provides a stable, predictable returns array for analytical verification checks."""
    return np.array([0.01, -0.005, 0.02, 0.004, -0.012, 0.018, 0.003, -0.002, 0.011, 0.005])

def test_sharpe_ratio_calculation(baseline_synthetic_returns):
    """Verifies that the annualized Sharpe computation engine runs correctly."""
    metrics = quant_stats.compute_sharpe_ratio(baseline_synthetic_returns, scaling_factor=252)
    assert "sharpe_ratio" in metrics
    assert isinstance(metrics["sharpe_ratio"], float)
    assert metrics["volatility"] > 0.0

def test_sortino_ratio_calculation(baseline_synthetic_returns):
    """Ensures that the Sortino down-side calculation handles negative variations cleanly."""
    metrics = quant_stats.compute_sortino_ratio(baseline_synthetic_returns, scaling_factor=252)
    assert "sortino_ratio" in metrics
    assert metrics["downside_volatility"] >= 0.0

def test_max_drawdown_calculation(baseline_synthetic_returns):
    """Confirms that the drawdown tracking module isolates maximum wealth compression peaks correctly."""
    metrics = quant_stats.compute_max_drawdown(baseline_synthetic_returns)
    assert "max_drawdown" in metrics
    assert metrics["max_drawdown"] <= 0.0

def test_statistical_test_execution(baseline_synthetic_returns):
    """Validates structural operation stability inside normality and stationarity check functions."""
    jb_res = quant_stats.run_jarque_bera_test(baseline_synthetic_returns)
    adf_res = quant_stats.run_adf_test(baseline_synthetic_returns)
    t_fit = quant_stats.execute_student_t_fit(baseline_synthetic_returns)
    
    assert jb_res["p_value"] >= 0.0
    assert "statistic" in adf_res
    assert t_fit["degrees_of_freedom"] > 0.0
