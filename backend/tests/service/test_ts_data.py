import backend.src.service import ts_data as td


def test_calc_integral_sum():
    # The case when input list is empty
    assert td.calc_integral_sum([]) == []

    # The case when integral sum is calculated correctly #1
    assert td.calc_integral_sum([120.8, 136.1, 178.1]) == [120.8, 256.9, 435.0]

    # The case when integral sum is calculated correctly #2
    assert td.calc_integral_sum([54.3, 49.6, 61.5]) == [54.3, 103.9, 165.4]

def test_calc_increase_percentage():
    # The case when input list is empty
    assert td.calc_increase_percentage([]) == []

    # The case when increase is calculated correctly #1
    assert td.calc_increase_percentage([20.0, 40.0, 50.0]) == [0.0, 100.0, 25.0]

    # The case when increase is calculated correctly #2
    assert td.calc_increase_percentage([128.0, 136.0, 255.0]) == [0.0, 6.25, 87.5]
