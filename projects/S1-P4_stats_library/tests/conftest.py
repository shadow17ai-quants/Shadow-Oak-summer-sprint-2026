import numpy as np
import pytest


@pytest.fixture
def constant_positive_returns():
    """20 days of constant +0.1% daily return -> known Sharpe/Sortino/Calmar."""
    return np.full(20, 0.001)


@pytest.fixture
def zero_returns():
    """All-zero returns -> edge case for every ratio."""
    return np.zeros(20)


@pytest.fixture
def known_drawdown_returns():
    """Goes up 10%, down 20%, up 5% -> drawdown is deterministic and hand-checkable."""
    return np.array([0.10, -0.20, 0.05])


@pytest.fixture
def normal_data():
    """Large sample from a true normal distribution -> should NOT reject normality."""
    rng = np.random.default_rng(42)
    return rng.normal(loc=0.0005, scale=0.01, size=2000)


@pytest.fixture
def non_normal_data():
    """Exponential distribution -> should reject normality clearly."""
    rng = np.random.default_rng(42)
    return rng.exponential(scale=0.01, size=2000) - 0.01


@pytest.fixture
def white_noise_data():
    """IID noise -> Ljung-Box should NOT find autocorrelation."""
    rng = np.random.default_rng(42)
    return rng.normal(0, 0.01, size=500)


@pytest.fixture
def autocorrelated_data():
    """AR(1) process with high persistence -> Ljung-Box SHOULD find autocorrelation."""
    rng = np.random.default_rng(42)
    n = 500
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = 0.8 * x[i - 1] + rng.normal(0, 0.01)
    return x


@pytest.fixture
def stationary_data():
    """Mean-reverting series -> ADF should find stationarity."""
    rng = np.random.default_rng(42)
    n = 300
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = 0.3 * x[i - 1] + rng.normal(0, 0.01)
    return x


@pytest.fixture
def random_walk_data():
    """Cumulative sum of noise -> ADF should NOT reject unit root (non-stationary)."""
    rng = np.random.default_rng(42)
    return np.cumsum(rng.normal(0, 0.01, size=300))


@pytest.fixture
def fat_tail_data():
    """Student-t with low df -> fit_student_t should recover low df (fat tails)."""
    rng = np.random.default_rng(42)
    return stats_t_rvs(df=3, size=2000, rng=rng)


def stats_t_rvs(df, size, rng):
    from scipy import stats as scipy_stats
    return scipy_stats.t.rvs(df=df, size=size, random_state=rng) * 0.01
