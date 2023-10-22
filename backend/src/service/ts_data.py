import requests
import apimoex
import pandas as pd
from service.converters import time_converter
from exceptions import MismatchSizeError


HALF_YEAR_IN_SECONDS = 6 * 30 * 24 * 60 * 60


def define_time_range_with_minimum_duration(start: str, end: str) -> (str, str):
    start_ts = time_converter.iso_to_timestamp(start)
    end_ts = time_converter.iso_to_timestamp(end)

    if end_ts - start_ts < HALF_YEAR_IN_SECONDS:
        end_ts = start_ts + HALF_YEAR_IN_SECONDS

    return time_converter.timestamp_to_iso(start_ts), time_converter.timestamp_to_iso(end_ts)


def get_values_with_timestamps(dates: list[str], values: list[float]) -> list[tuple[int, float]]:
    if len(dates) != len(values):
        raise MismatchSizeError

    values_with_timestamps: list[tuple[float, float]] = []
    for i in range(len(dates)):
        values_with_timestamps.append((int(time_converter.iso_to_timestamp(dates[i])), values[i]))

    return values_with_timestamps


def get_historical_information(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Get historical ticker's data by api request from moex.com"""

    with requests.Session() as session:
        features: pd.DataFrame = pd.DataFrame(apimoex.find_securities(session, ticker,
        columns=('secid', 'group', 'primary_boardid')))
        engine, market = features.loc[features['secid'] == ticker].group.values[0].split('_')
        board: str = features.loc[features.secid == ticker].primary_boardid.values[0]
        df = pd.DataFrame(apimoex.get_board_history(session, ticker, start=start_date, end=end_date,
                                        columns=('TRADEDATE', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'MARKETPRICE2'),
                                        board=board, market=market, engine=engine))
        df = df.dropna()
        df = df.reset_index(drop=True)
        return df

def calc_integral_sum(df: pd.DataFrame, column: str = 'OPEN') -> pd.DataFrame:
    """
    :param df:
        a pandas.DataFrame
    :param column:
        the name of the column for which the calculation is performed
    :return:
        a pandas.DataFrame with a newly calculated column
    """

    if df.empty or column not in df.columns.to_list():
        return pd.DataFrame()
    df['integ_val'] = df[column].expanding(min_periods=1).sum()
    return df

def calc_increase_percentage(df: pd.DataFrame) -> list[float]:
    if df.empty:
        return []
    df['inc_perc'] = round((df.integ_val / df.integ_val.shift(1) - 1) * 100, 2)
    df.inc_perc = df.inc_perc.fillna(0)
    return df.inc_perc.to_list()