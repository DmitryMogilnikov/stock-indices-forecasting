import requests
import apimoex
import pandas as pd
from typing import Union


def get_ticker_feature(ticker: str, session: requests.Session()) -> tuple[str, str, str]:
    """
    :return:
        (engine, market, board)"""

    features: pd.DataFrame = pd.DataFrame(apimoex.find_securities(session, ticker,
                                                                  columns=('secid', 'group', 'primary_boardid')))
    engine, market = features.loc[features['secid'] == ticker].group.values[0].split('_')
    board: str = features.loc[features.secid == ticker].primary_boardid.values[0]
    return engine, market, board

def get_historical_information(ticker: str, start_date: str,
                               end_date: str, session: requests.Session()) \
        -> list[dict[str, tuple[str, int, float]]]:
    """get historical ticker's data by api request from moex.com
    :return: a list of dictionaries that can be easily converted to a pandas.DataFrame"""

    engine, market, board = get_ticker_feature(ticker, session)
    return apimoex.get_board_history(session, ticker, start=start_date, end=end_date,
                                     columns=('TRADEDATE', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VALUE', 'CAPITALIZATION'),
                                     board=board, market=market, engine=engine)

def calc_integral_sum(data: list[dict[str, Union[str, int, float]]]) -> pd.DataFrame():
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame()
    df['integ_val'] = df.OPEN.expanding(min_periods=1).sum()
    return df

def calc_increase_percentage(df: pd.DataFrame) -> list[float]:
    if df.empty:
        return []
    df['inc_perc'] = round((df.integ_val / df.integ_val.shift(1) - 1) * 100, 2)
    df.inc_perc = df.inc_perc.fillna(0)
    return list(df.inc_perc.to_numpy())
