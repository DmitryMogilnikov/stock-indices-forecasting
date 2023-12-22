import pytest
import unittest
from unittest.mock import MagicMock, patch, call
from backend.src.service import moex
import pandas as pd


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


def test_get_values_with_dates():
    # Case with invalid date format
    with pytest.raises(Exception) as err:
        moex.get_values_with_dates(
            ["2023:01?01", "2023-01-02"],
            [0.5, 0.4]
        )
    assert str(err.value) == "Invalid isoformat string: '2023:01?01'"

    # Case where len(dates) != len(values)
    with pytest.raises(Exception) as err:
        moex.get_values_with_dates(["2023-01-01", "2023-01-02"], [0.5])
    assert str(err.value) == "Mismatched sizes of dates and values error"

    # Correct case
    unittest.TestCase().assertListEqual(
        list1=moex.get_values_with_dates(
            ["2023-01-01", "2023-01-02"],
            [0.5, 0.4]
        ),
        list2=[
            (1672522200000, 0.5),
            (1672608600000, 0.4)
        ]
    )

    # Case with empty lists
    assert moex.get_values_with_dates([], []) == []

def test_find_moex_security():
    session_mock = MagicMock()
    ticker = "AAPL"
    with patch('apimoex.find_securities') as find_securities_mock:
        find_securities_mock.return_value = [{'secid': 'AAPL', 'group': 'stock_shares', 'primary_boardid': 'TQBR'}]
        result = moex.find_moex_security(session_mock, ticker)
        expected_result = pd.DataFrame([{'secid': 'AAPL', 'group': 'stock_shares', 'primary_boardid': 'TQBR'}])
        pd.testing.assert_frame_equal(result, expected_result)

def test_get_engine_and_market():
    features_mock = pd.DataFrame({'secid': ['AAPL'], 'group': ['stock_shares'], 'primary_boardid': ['TQBR']})
    ticker = 'AAPL'
    result = moex.get_engine_and_market(features_mock, ticker)
    assert result == ('stock', 'shares')

def test_get_board_id():
    features_mock = pd.DataFrame({'secid': ['AAPL'], 'primary_boardid': ['TQBR']})
    ticker = 'AAPL'
    result = moex.get_board_id(features_mock, ticker)
    assert result == 'TQBR'

def test_get_board_history():
    session_mock = MagicMock()
    ticker = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2022-01-05'
    board_mock = 'TQBR'
    market_mock = 'shares'
    engine_mock = 'stock'
    with patch('apimoex.get_board_history') as get_board_history_mock:
        get_board_history_mock.return_value = pd.DataFrame({
            'TRADEDATE': ['2022-01-01', '2022-01-02'],
            'OPEN': [100, 110],
            'CLOSE': [105, 115],
            'HIGH': [120, 125],
            'LOW': [95, 105]
        })
        result = moex.get_board_history(
            session_mock,
            ticker,
            start_date,
            end_date,
            board_mock,
            market_mock,
            engine_mock
        )
        expected_result = pd.DataFrame({
            'TRADEDATE': ['2022-01-01', '2022-01-02'],
            'OPEN': [100, 110],
            'CLOSE': [105, 115],
            'HIGH': [120, 125],
            'LOW': [95, 105]
        })
        pd.testing.assert_frame_equal(result, expected_result)

def test_filter_and_reset_dataframe():
    df_mock = pd.DataFrame({
        'TRADEDATE': ['2022-01-01', '2022-01-02'],
        'OPEN': [100, 110],
        'CLOSE': [105, 115],
        'HIGH': [120, 125],
        'LOW': [95, 105]
    })
    result = moex.filter_and_reset_dataframe(df_mock)
    expected_result = pd.DataFrame({
        'TRADEDATE': ['2022-01-01', '2022-01-02'],
        'OPEN': [100, 110],
        'CLOSE': [105, 115],
        'HIGH': [120, 125],
        'LOW': [95, 105]
    })
    pd.testing.assert_frame_equal(result, expected_result)

def test_get_historical_information():
    with patch('requests.Session') as session_mock:
        ticker = "AAPL"
        start_date = "2022-01-01"
        end_date = "2022-02-01"
        features_mock = pd.DataFrame({'secid': ['AAPL'], 'group': ['stock_shares'], 'primary_boardid': ['TQBR']})
        with patch('backend.src.service.moex.find_moex_security', return_value=features_mock):
            get_board_history_mock = pd.DataFrame({
                'TRADEDATE': ['2022-01-01', '2022-01-02'],
                'OPEN': [100, 110],
                'CLOSE': [105, 115],
                'HIGH': [120, 125],
                'LOW': [95, 105]
            })
            with patch('backend.src.service.moex.get_board_history', return_value=get_board_history_mock):
                result = moex.get_historical_information(ticker, start_date, end_date)
                expected_result = pd.DataFrame({
                    'TRADEDATE': ['2022-01-01', '2022-01-02'],
                    'OPEN': [100, 110],
                    'CLOSE': [105, 115],
                    'HIGH': [120, 125],
                    'LOW': [95, 105]
                })
                pd.testing.assert_frame_equal(result, expected_result)

def test_add_data_by_ticker():
    with patch('backend.src.service.moex.define_time_range_with_minimum_duration', return_value=("2022-01-01", "2022-02-01")) as define_time_range_mock, \
         patch('backend.src.service.moex.get_historical_information') as get_historical_information_mock, \
         patch('backend.src.service.moex.get_values_with_dates') as get_values_with_dates_mock:

        ts_api_mock = MagicMock()
        ticker = "AAPL"
        start_date = "2022-01-01"
        end_date = "2022-02-01"

        get_historical_information_mock.return_value = pd.DataFrame({
            'TRADEDATE': ['2022-01-01', '2022-01-02'],
            'OPEN': [100, 110],
            'CLOSE': [100, 110],
            'HIGH': [100, 110],
            'LOW': [100, 110]
        })

        get_values_with_dates_mock.return_value = [(1640995200, 100), (1641081600, 110)]

        moex.add_data_by_ticker(ts_api_mock, ticker, start_date, end_date)

        expected_calls = [
            call(ticker, 'OPEN', [(1640995200, 100), (1641081600, 110)]),
            call(ticker, 'CLOSE', [(1640995200, 100), (1641081600, 110)]),
            call(ticker, 'MAX', [(1640995200, 100), (1641081600, 110)]),
            call(ticker, 'MIN', [(1640995200, 100), (1641081600, 110)])
        ]

        ts_api_mock.add_points.assert_has_calls(expected_calls, any_order=True)
