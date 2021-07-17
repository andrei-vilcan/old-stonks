# import pandas as pd
# from alpha_vantage.timeseries import TimeSeries
import yfinance as yf

# key = 'OI6MT7LTU8SGRQ43'
# ts = TimeSeries(key, output_format='pandas')

def get_data(ticker_: str, timeframe: str):
    # try:
    #     data, meta = ts.get_intraday(ticker_, interval='30min', outputsize='full')
    #     return data
    # except:
    #     pass
    period = ''
    if timeframe in ['1d', '1wk', '1mo', '1h']:
        period = '240d'
    else:
        period = '60d'
    try:
        stock_df = yf.download(tickers=ticker_,
                               period=period,
                               interval=timeframe,
                               auto_adjust=True)
        return stock_df
    except:
        pass