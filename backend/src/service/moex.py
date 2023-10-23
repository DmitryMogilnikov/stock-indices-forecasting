import requests
import apimoex
import pandas as pd
import numpy as np
from service.converters import time_converter
from exceptions import MismatchSizeError, moex
from datetime import timedelta


def define_time_range_with_minimum_duration(
    start: str,
    end: str
) -> tuple[str, str]:
    try:
        start = time_converter.str_to_iso(start)
        end = time_converter.str_to_iso(end)
    except ValueError as err:
        raise moex.InvalidDateFormat(err)

    end = max(end, start + timedelta(days=180))

    return (time_converter.iso_to_str(start), time_converter.iso_to_str(end))


def get_values_with_timestamps(
    dates: list[str],
    values: list[float]
) -> list[tuple[int, float]]:
    try:
        dates = np.vectorize(time_converter.iso_to_timestamp)(dates)
    except ValueError:
        return []

    try:
        dates_with_values = np.column_stack([dates, values])
    except Exception:
        raise MismatchSizeError('Mismatched sizes of dates and values error')

    return [tuple(date_with_value) for date_with_value in dates_with_values]


def find_moex_security(session, ticker):
    """Find security details for the given ticker."""
    return pd.DataFrame(
        apimoex.find_securities(
            session,
            ticker,
            columns=('secid', 'group', 'primary_boardid')
        )
    )


def get_engine_and_market(features, ticker):
    """Extract engine and market information based on the ticker."""
    engine, market = features.loc[
        features['secid'] == ticker
    ].group.values[0].split('_')
    return engine, market


def get_board_id(features, ticker):
    """Get the primary board ID for the given ticker."""
    return features.loc[features.secid == ticker].primary_boardid.values[0]


def get_board_history(
    session,
    ticker,
    start_date,
    end_date,
    board,
    market,
    engine
):
    """Retrieve historical data for the ticker from the board."""
    return pd.DataFrame(
        apimoex.get_board_history(
            session,
            ticker,
            start=start_date,
            end=end_date,
            columns=(
                'TRADEDATE',
                'OPEN',
                'CLOSE',
                'HIGH',
                'LOW',
                'MARKETPRICE2'
            ),
            board=board, market=market, engine=engine
        )
    )


def filter_and_reset_dataframe(df):
    """Filter out rows with NaN values and reset the DataFrame index."""
    df = df.dropna()
    return df.reset_index(drop=True)


def get_historical_information(ticker, start_date, end_date):
    """Get historical ticker's data by API request from moex.com."""
    with requests.Session() as session:
        features = find_moex_security(session, ticker)

        if features.empty:
            raise moex.TickerNotFoundError(f"Ticker not found: {ticker}")

        try:
            engine, market = get_engine_and_market(features, ticker)
        except IndexError:
            raise moex.TickerNotFoundError(f"Ticker not found: {ticker}")

        board = get_board_id(features, ticker)

        df = get_board_history(
            session,
            ticker,
            start_date,
            end_date,
            board,
            market,
            engine
        )
        df = filter_and_reset_dataframe(df)

        if df.empty:
            raise moex.DataNotFoundForThisTime(
                f"Data not found for this time: from {start_date} to {end_date}"
            )

        return df
