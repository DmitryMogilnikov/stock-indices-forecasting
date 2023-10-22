import pytest
from backend.src.service import ts_data
from backend.src.exceptions import MismatchSizeError

def test_define_time_range_with_minimum_duration():
    # Case where the start is less than end on half a year
    assert ts_data.define_time_range_with_minimum_duration("2023-01-01", "2023-01-31") == ("2023-01-01", "2023-06-30")

    # Case where the start is longer than end on half a year
    assert ts_data.define_time_range_with_minimum_duration("2023-01-01", "2023-08-01") == ("2023-01-01", "2023-08-01")

def test_get_values_with_timestamps():
    # Case where len(dates) != len(values)
    with pytest.raises(MismatchSizeError):
        ts_data.get_values_with_timestamps(["2023-01-01", "2023-01-02"], [0.5])
    
    # Correct case
    assert ts_data.get_values_with_timestamps(["2023-01-01", "2023-01-02"], [0.5, 0.4]) == [(1672522200, 0.5), (1672608600, 0.4)]

    # Case with empty lists
    assert ts_data.get_values_with_timestamps([], []) == []
