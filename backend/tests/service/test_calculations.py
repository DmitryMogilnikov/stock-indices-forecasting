import pytest as pytest
import numpy as np


from backend.src.service import calculations


@pytest.mark.parametrize(
    'initial_percent, percent_value, target_reduction, expected_result',
    [(4.59, 3.41, 1.0, True),
     (4.59,3.82,1.0, False),
     (3.82,4.59,1.0, False)
     ]
)
def test_is_reduction_sufficient(initial_percent, percent_value, target_reduction, expected_result):
    assert np.array_equal(calculations.is_reduction_sufficient(initial_percent, percent_value, target_reduction), expected_result)


@pytest.mark.parametrize(
    'percentage_changes, initial_percent, target_reduction, expected_result',
    [([], 4.60, 0.6, 0),
     ([4.59, 4.21, 3.89, 2.47], 4.60, 0.6, 3),
     ([4.59, 4.21, 3.89, 2.47], 4.60, 1.0, 4),
     ([4.59, 4.21, 3.89, 2.47], 4.60, 5.0, 0)
     ]
)
def test_get_days_to_reduce_procent(percentage_changes, initial_percent, target_reduction, expected_result):
    assert np.array_equal(calculations.get_days_to_reduce_procent(percentage_changes, initial_percent, target_reduction), expected_result)


@pytest.mark.parametrize(
    'percentage_changes, target_reduction, expected_result',
    [([], 0.6, []),
     ([4.59, 4.21, 3.89, 2.47], 0.6, [2, 2, 1, 0]),
     ([4.59, 4.21, 3.89, 2.47], 5.0, [0, 0, 0, 0]),
     ([4.59, 4.21, 3.89, 2.47], 0.1, [1, 1, 1, 0]),
     ([4.59, 4.21, 3.89, 2.47], 2.1, [3, 0, 0, 0])
     ]
)
def test_calculate_days_to_target_reductions(percentage_changes, target_reduction, expected_result):
    assert np.array_equal(calculations.calculate_days_to_target_reduction(percentage_changes, target_reduction), expected_result)


@pytest.mark.parametrize(
    'data, expected_result',
    [([], np.array(0.0)),
     ([120.8, 136.1, 178.1], np.array([120.8, 256.9, 435.0])),
     ([54.3, 49.6, 61.5], np.array([54.3, 103.9, 165.4]))
     ]
)
def test_calc_integral_sum(data, expected_result):
    assert np.array_equal(calculations.calc_integral_sum(data), expected_result)


@pytest.mark.parametrize(
    'data, expected_result',
    [(np.array([]), np.array(0.0)),
     (np.array([20.0, 40.0, 50.0]), np.array([0.0, 100.0, 25.0])),
     (np.array([128.0, 136.0, 255.0]), np.array([0.0, 6.25, 87.5]))
     ]
)
def test_calc_increase_percentage(data, expected_result):
    assert np.array_equal(calculations.calc_increase_percentage(data), expected_result)
