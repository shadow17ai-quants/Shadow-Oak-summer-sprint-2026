# S1-P4: Financial Statistics Library v0.1 Framework Component
"""
Unified mathematical calculation matrix framework containing primary risk metrics 
and non-parametric significance testing routines.
"""
import numpy as np
import scipy.stats as stats
from typing import Dict, Tuple

def compute_sharpe_ratio(returns_vector: np.ndarray, scaling_factor: int = 252) -> Dict[str, float]:
    """Computes standard annualized risk-adjusted outperformance metrics."""
    mean_val = np.mean(returns_vector)
    sigma_val = np.std(returns_vector, ddof=1)
    ratio = (mean_val / sigma_val) * np.sqrt(scaling_factor) if sigma_val > 0 else 0.0
    return {"sharpe_ratio": float(ratio), "mean_return": float(mean_val), "volatility": float(sigma_val)}

def compute_sortino_ratio(returns_vector: np.ndarray, scaling_factor: int = 252) -> Dict[str, float]:
    """Calculates down-side risk profiling dynamics excluding upside variance footprints."""
    mean_val = np.mean(returns_vector)
    downside_returns = returns_vector[returns_vector < 0.0]
    downside_sigma = np.std(downside_returns, ddof=1) if len(downside_returns) > 1 else 0.0
    ratio = (mean_val / downside_sigma) * np.sqrt(scaling_factor) if downside_sigma > 0 else 0.0
    return {"sortino_ratio": float(ratio), "downside_volatility": float(downside_sigma)}

def compute_max_drawdown(returns_vector: np.ndarray) -> Dict[str, float]:
    """Calculates peak-to-trough capital compression percentages."""
    cumulative_wealth = np.exp(np.cumsum(returns_vector))
    running_peaks = np.maximum.accumulate(cumulative_wealth)
    drawdowns = (cumulative_wealth - running_peaks) / running_peaks
    max_dd = np.min(drawdowns) if len(drawdowns) > 0 else 0.0
    return {"max_drawdown": float(max_dd)}

def compute_calmar_ratio(returns_vector: np.ndarray, scaling_factor: int = 252) -> Dict[str, float]:
    """Computes annualized performance tracking over peak systemic drawdown parameters."""
    annualized_return = np.mean(returns_vector) * scaling_factor
    max_dd_metric = abs(compute_max_drawdown(returns_vector)["max_drawdown"])
    ratio = (annualized_return / max_dd_metric) if max_dd_metric > 0 else 0.0
    return {"calmar_ratio": float(ratio)}

def compute_omega_ratio(returns_vector: np.ndarray, minimum_acceptable_threshold: float = 0.0) -> Dict[str, float]:
    """Calculates the area ratio of positive probability outcomes relative to negative benchmarks."""
    excess_gains = returns_vector - minimum_acceptable_threshold
    gains_sum = np.sum(excess_gains[excess_gains > 0.0])
    losses_sum = np.sum(np.abs(excess_gains[excess_gains < 0.0]))
    ratio = (gains_sum / losses_sum) if losses_sum > 0 else 0.0
    return {"omega_ratio": float(ratio)}

# --- Statistical Inference Validation Infrastructure Testing Section ---
def run_jarque_bera_test(returns_vector: np.ndarray) -> Dict[str, float]:
    """Tests sample alignment matching normal distribution boundary conditions via skewness/kurtosis tracking."""
    stat_val, p_val = stats.jarque_bera(returns_vector)
    return {"statistic": float(stat_val), "p_value": float(p_val)}

def run_shapiro_wilk_test(returns_vector: np.ndarray) -> Dict[str, float]:
    """Tests normalcy assumptions across short tracking sequences."""
    stat_val, p_val = stats.shapiro(returns_vector)
    return {"statistic": float(stat_val), "p_value": float(p_val)}

def run_ljung_box_test(returns_vector: np.ndarray, target_lags: int = 10) -> Dict[str, float]:
    """Evaluates serial return correlation structures to check for remaining asset memory signatures."""
    # Use localized calculations bypassing complex multi-index tables
    from statsmodels.stats.diagnostic import acorr_ljungbox
    dataframe_res = acorr_ljungbox(returns_vector, lags=[target_lags], return_df=True)
    stat_val = dataframe_res.iloc[0, 0]
    p_val = dataframe_res.iloc[0, 1]
    return {"statistic": float(stat_val), "p_value": float(p_val)}

def run_adf_test(returns_vector: np.ndarray) -> Dict[str, float]:
    """Validates data convergence stationarity profiles to prevent spurious relationship models."""
    from statsmodels.tsa.stattools import adfuller
    stat_val, p_val, _, _, _, _ = adfuller(returns_vector)
    return {"statistic": float(stat_val), "p_value": float(p_val)}

def execute_student_t_fit(returns_vector: np.ndarray) -> Dict[str, float]:
    """Fits degrees-of-freedom curves to log returns to detect fat-tail anomalies."""
    df_parameter, localization_param, scaling_param = stats.t.fit(returns_vector)
    return {"degrees_of_freedom": float(df_parameter), "location": float(localization_param), "scale": float(scaling_param)}
