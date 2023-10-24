import pytest
import unittest
from backend.src.service import moex


def test_define_time_range_with_minimum_duration():
    # Case with invalid date format
    with pytest.raises(Exception) as err:
        moex.define_time_range_with_minimum_duration(
            "2023:01?01",
            "2023-01-02"
        )
    assert str(err.value) == "time data '2023:01?01' does not match format '%Y-%m-%d'"

    # Case where start is greater that end
    with pytest.raises(Exception) as err:
        moex.define_time_range_with_minimum_duration(
            "2029-01-01",
            "2023-01-02"
        )
    assert str(err.value) == "start (2029-01-01) cannot be greater than end (2023-01-02)"

    # Case where the start is less than end on half a year
    assert moex.define_time_range_with_minimum_duration(
        "2023-06-30",
        "2023-07-30"
    ) == (
        "2023-01-31",
        "2023-07-30"
    )

    # Case where the start is longer than end on half a year
    assert moex.define_time_range_with_minimum_duration(
        "2023-01-01",
        "2023-08-01"
    ) == (
        "2023-01-01",
        "2023-08-01"
    )


def test_get_values_with_timestamps():
    # Case with invalid date format
    with pytest.raises(Exception) as err:
        moex.get_values_with_timestamps(
            ["2023:01?01", "2023-01-02"],
            [0.5, 0.4]
        )
    assert str(err.value) == "Invalid isoformat string: '2023:01?01'"

    # Case where len(dates) != len(values)
    with pytest.raises(Exception) as err:
        moex.get_values_with_timestamps(["2023-01-01", "2023-01-02"], [0.5])
    assert str(err.value) == "Mismatched sizes of dates and values error"

    # Correct case
    unittest.TestCase().assertListEqual(
        list1=moex.get_values_with_timestamps(
            ["2023-01-01", "2023-01-02"],
            [0.5, 0.4]
        ),
        list2=[
            (1672522200000, 0.5),
            (1672608600000, 0.4)
        ]
    )

    # Case with empty lists
    assert moex.get_values_with_timestamps([], []) == []
