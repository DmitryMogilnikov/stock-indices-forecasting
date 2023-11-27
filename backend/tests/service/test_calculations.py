import pytest as pytest
import numpy as np

from backend.src.service import calculations


def mock_get_range(name, start, end, prefix):
    if name == "test_index_1":
        return np.array([[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]])
    if name == "test_index_2":
        return np.array([[1, 0.5], [2, 0.3], [3, 0.15], [4, 0.1], [5, 0.05]])


@pytest.fixture
def calculation_index_instance(request):
    name = request.param
    calculations.ts_api.get_range = lambda name, start, end, prefix: mock_get_range(name, start, end, prefix)
    return calculations.CalculationIndex(index_name=name, prefix="test_prefix", start=0, end=5)


@pytest.mark.parametrize("calculation_index_instance", ["test_index_1", "test_index_2"], indirect=True)
def test_calc_integral_sum(calculation_index_instance):
    calculation_index_instance.calc_integral_sum()
    assert np.allclose(calculation_index_instance.integral_sum, np.array([5, 9, 12, 14, 15])) \
        if calculation_index_instance.index_name == "test_index_1" \
        else np.allclose(calculation_index_instance.integral_sum, np.array([0.5, 0.8, 0.95, 1.05, 1.1]))


@pytest.mark.parametrize("calculation_index_instance", ["test_index_1", "test_index_2"], indirect=True)
def test_calc_increase_percentage(calculation_index_instance):
    calculation_index_instance.calc_integral_sum()
    calculation_index_instance.calc_increase_percentage()
    assert np.allclose(calculation_index_instance.increase_percentage, np.array([0.0, 80.0, 33.33333333, 16.66666667, 7.14285714])) \
        if calculation_index_instance.index_name == "test_index_1" \
        else np.allclose(calculation_index_instance.increase_percentage, np.array([0.0, 60.0, 18.75, 10.52631579, 4.76190476]))


@pytest.mark.parametrize("calculation_index_instance", ["test_index_1", "test_index_2"], indirect=True)
def test_calc_days_to_target_reduction(calculation_index_instance):
    if calculation_index_instance.index_name == "test_index_1":
        calculation_index_instance.reduction = 11
        calculation_index_instance.tolerance = 1e-6
    else:
        calculation_index_instance.reduction = 50
        calculation_index_instance.tolerance = 1e-6

    calculation_index_instance.calc_integral_sum()
    calculation_index_instance.calc_increase_percentage()
    calculation_index_instance.calc_days_to_target_reduction()
    assert np.allclose(calculation_index_instance.days_to_reduction, np.array([0.0, 0.0, 1.0, 1.0, 0.0])) \
        if calculation_index_instance.index_name == "test_index_1" \
        else np.allclose(calculation_index_instance.days_to_reduction, np.array([0.0, 0.0, 0.0, 0.0, 3.0]))
