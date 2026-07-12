# S1-P4: Financial Statistics Library v0.1

Shadow Oak Capitals sprint deliverable. Standardised analytical engine used by every paper and backtest going forward.

## Install

```powershell
pip install -e .
```

## Functions (Ratios) — `quant_stats.ratios`

| Function | Input | Output | Interpretation |
|---|---|---|---|
| `sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252)` | array of period returns | dict: `sharpe_ratio`, `annualized_return`, `annualized_volatility` | Risk-adjusted return per unit of total volatility. Higher is better. |
| `sortino_ratio(returns, risk_free_rate=0.0, periods_per_year=252)` | array of period returns | dict: `sortino_ratio`, `annualized_return`, `downside_deviation` | Like Sharpe but only penalises downside volatility. |
| `calmar_ratio(returns, periods_per_year=252)` | array of period returns | dict: `calmar_ratio`, `annualized_return`, `max_drawdown` | Annualised return divided by worst drawdown. |
| `omega_ratio(returns, threshold=0.0)` | array of period returns | dict: `omega_ratio`, `gains_sum`, `losses_sum` | Ratio of total gains to total losses above/below a threshold. |
| `max_drawdown(returns)` | array of period returns | dict: `max_drawdown`, `peak_index`, `trough_index` | Largest peak-to-trough decline in cumulative value. |

## Functions (Hypothesis Tests) — `quant_stats.hypothesis_tests`

| Function | Input | Output | Interpretation |
|---|---|---|---|
| `jarque_bera_test(returns)` | array of returns | dict: `statistic`, `p_value`, `interpretation` | Tests normality via skewness/kurtosis. p < 0.05 → not normal. |
| `shapiro_wilk_test(returns)` | array of returns | dict: `statistic`, `p_value`, `interpretation` | Tests normality, more powerful for small samples. p < 0.05 → not normal. |
| `ljung_box_test(returns, lags=10)` | array of returns | dict: `statistic`, `p_value`, `interpretation` | Tests for autocorrelation. p < 0.05 → significant autocorrelation. |
| `adf_test(returns)` | array of returns | dict: `statistic`, `p_value`, `interpretation` | Augmented Dickey-Fuller unit root test. p < 0.05 → stationary. |
| `fit_student_t(returns)` | array of returns | dict: `statistic`, `p_value`, `degrees_of_freedom`, `loc`, `scale`, `interpretation` | Fits Student-t distribution. df < 5 = extreme fat tails, 5-10 = moderate, >10 = near-normal. |

## Combined report

```python
from quant_stats import full_report
report = full_report(log_returns)
```

Returns all 10 functions' results in one dict, keyed by function name.

## Apply to Nifty 50 data

```powershell
python scripts/apply_to_nifty.py
```

Reads the CSV already downloaded by S1-P2 (`nifftyvault`), computes daily log returns, and prints every function''s output.

## Testing

```powershell
pytest
```

Full suite runs against synthetic data with known correct outputs — constant returns, known drawdown sequences, true-normal vs. non-normal samples, white noise vs. autocorrelated series, random walk vs. stationary series, and low-df Student-t samples.

## Limitations

- `ljung_box_test` and `adf_test` require `statsmodels`.
- Shapiro-Wilk is capped at 5000 samples per scipy''s reliability limit.
- All ratio functions assume `returns` are simple/log period returns, not prices — pass log returns for consistency with the rest of the sprint.
