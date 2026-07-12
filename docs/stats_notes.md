# Statistics Notes – p‑values, t‑tests, Confidence Intervals

## p‑value

- Probability of observing a result as extreme as (or more extreme than) the one observed, assuming the null hypothesis is true.
- Small p‑value (< 0.05) → evidence against the null → reject null.
- Used in hypothesis testing for signals (e.g., Sharpe ratio > 0).

---

## t‑test

- Tests whether the mean of a sample is significantly different from a known value (or from another sample).
- Formula (one‑sample):

$$ t = \frac{\bar{x} - \mu}{s / \sqrt{n}} $$

- \( \bar{x} \) = sample mean, \( \mu \) = population mean, \( s \) = sample std, \( n \) = sample size.

---

## Confidence Interval (CI)

- Range within which the true population parameter is expected to lie with a certain confidence level (e.g., 95%).
- For Sharpe ratio, we bootstrap to get a 95% CI.
- Wider CI → more uncertainty.

---

## Bootstrap

- Resample the data (with replacement) many times (e.g., 10,000).
- Compute the statistic (e.g., Sharpe) on each resample.
- The 2.5th and 97.5th percentiles give the 95% CI.