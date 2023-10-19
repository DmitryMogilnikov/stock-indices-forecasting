import requests
import apimoex
import pandas as pd


with requests.Session() as session:
    ticker = 'IMOEX'
    start = '2023-09-15'
    end = '2023-10-18'
    features = pd.DataFrame(apimoex.find_securities(session, ticker, columns=('secid', 'group', 'primary_boardid')))
    engine, market = features.loc[features['secid'] == ticker].group.values[0].split('_')
    board = features.loc[features.secid == ticker].primary_boardid.values[0]
    data = apimoex.get_board_history(session, ticker, start=start, end=end,
                                     columns=('TRADEDATE', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VALUE', 'CAPITALIZATION'),
                                     board=board, market=market, engine=engine)
    df = pd.DataFrame(data)
    if not df.empty:
        df.TRADEDATE = pd.to_datetime(df.TRADEDATE)
        df.set_index('TRADEDATE', inplace=True)
        df['integ_val'] = df.OPEN.expanding(min_periods=1).sum()  # integral sum of opening price
        df['inc_perc'] = round((df.integ_val / df.integ_val.shift(1) - 1) * 100, 2)  # increase percentage
        df.inc_perc = df.inc_perc.fillna(0)
