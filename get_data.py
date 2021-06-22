import yfinance as yf

def get_data(ticker_: str, period_: str, timeframe: str):
    stock_df = yf.download(tickers=ticker_,
                                period=period_,
                                interval=timeframe,
                                auto_adjust=True)
    # example usage:
    # intraday_data = yf.download(tickers="MSFT",
    #                             period="30d",
    #                             time_frame="1m",
    #                             auto_adjust=True)
    return stock_df
