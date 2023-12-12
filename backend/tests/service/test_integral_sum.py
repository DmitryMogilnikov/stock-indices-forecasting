import pytest as pytest

import backend.src.service.integral_sum as td


@pytest.mark.parametrize(
    'data, expected_result',
    [([], td.np.array(0.0)),
     ([120.8, 136.1, 178.1], td.np.array([120.8, 256.9, 435.0])),
     ([54.3, 49.6, 61.5], td.np.array([54.3, 103.9, 165.4]))
     ]
)
def test_calc_integral_sum(data, expected_result):
    assert td.np.array_equal(td.calc_integral_sum(data), expected_result)

@pytest.mark.parametrize(
    'data, expected_result',
    [(td.np.array([]), td.np.array(0.0)),
     (td.np.array([20.0, 40.0, 50.0]), td.np.array([0.0, 100.0, 25.0])),
     (td.np.array([128.0, 136.0, 255.0]), td.np.array([0.0, 6.25, 87.5]))
     ]
)
def test_calc_increase_percentage(data, expected_result):
    assert td.np.array_equal(td.calc_increase_percentage(data), expected_result)
