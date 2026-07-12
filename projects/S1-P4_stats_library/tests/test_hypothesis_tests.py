import numpy as np
from quant_stats.hypothesis_tests import (
    jarque_bera_test,
    shapiro_wilk_test,
    ljung_box_test,
    adf_test,
    fit_student_t,
)


def test_jarque_bera_normal_data(normal_data):
    result = jarque_bera_test(normal_data)
    assert result["p_value"] > 0.05
    assert "cannot reject" in result["interpretation"]


def test_jarque_bera_non_normal_data(non_normal_data):
    result = jarque_bera_test(non_normal_data)
    assert result["p_value"] < 0.05
    assert "NOT normally" in result["interpretation"]


def test_shapiro_wilk_normal_data(normal_data):
    result = shapiro_wilk_test(normal_data)
    assert result["p_value"] > 0.05


def test_shapiro_wilk_non_normal_data(non_normal_data):
    result = shapiro_wilk_test(non_normal_data)
    assert result["p_value"] < 0.05


def test_ljung_box_white_noise(white_noise_data):
    result = ljung_box_test(white_noise_data, lags=10)
    assert result["p_value"] > 0.05
    assert "no significant" in result["interpretation"]


def test_ljung_box_autocorrelated(autocorrelated_data):
    result = ljung_box_test(autocorrelated_data, lags=10)
    assert result["p_value"] < 0.05
    assert "significant autocorrelation" in result["interpretation"]


def test_adf_stationary_series(stationary_data):
    result = adf_test(stationary_data)
    assert result["p_value"] < 0.05
    assert (
        "stationary" in result["interpretation"]
        and "NOT" not in result["interpretation"]
    )


def test_adf_random_walk(random_walk_data):
    result = adf_test(random_walk_data)
    assert result["p_value"] > 0.05
    assert "NOT stationary" in result["interpretation"]


def test_fit_student_t_fat_tails(fat_tail_data):
    result = fit_student_t(fat_tail_data)
    assert result["degrees_of_freedom"] < 10
    assert "fat tails" in result["interpretation"]


def test_insufficient_data_all_functions():
    tiny = np.array([0.01])
    assert np.isnan(jarque_bera_test(tiny)["statistic"])
    assert np.isnan(shapiro_wilk_test(tiny)["statistic"])
    assert np.isnan(ljung_box_test(tiny)["statistic"])
    assert np.isnan(adf_test(tiny)["statistic"])
    assert np.isnan(fit_student_t(tiny)["statistic"])
