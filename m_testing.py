from stock import Stock
# from reddit_scraper import tickers_letters_only
import numpy as np
import matplotlib.pyplot as plt

cm = plt.cm.get_cmap('RdYlGn')
tickers = ['amd']
total_gains = []

for ticker in tickers:
    try:

        stock = Stock(ticker, period='7d', timeframes='5m')
        prices = list(stock.charts['30m'].closes)
        colours = list(stock.charts['30m'].combined_scales())

        inTrade = False
        cash = 1000
        entry_point = 0
        exit_point = 0

        plt.scatter(x=range(len(prices)), y=prices, c=colours, cmap=cm)

        for i in range(len(prices)):
            if not inTrade:
                # Enter trade if green enough, record entry price
                if colours[i] > 0.55:
                    entry_point = prices[i]
                    plt.axvline(x=i, color='g')
                    inTrade = True
            elif inTrade:
                # Exit trade if red enough
                if colours[i] <= 0.45:
                    exit_point = prices[i]
                    inTrade = False
                    cash = cash * (1 + ((exit_point - entry_point) / entry_point))
                    plt.axvline(x=i, color='r')
        total_gains.append((cash - 1000) / 1000)
        plt.show()
    except Exception as e:
        print(e)
        pass


# tickers = ['btc-usd']
# for stock in tickers:
#     stock = Stock(stock)
#     data = list(stock.charts['1h'].closes)
#     colours = stock.charts['1h'].combined_scales()
#     # colours = stock.charts['1d'].combined_scales()
#
#     cm = plt.cm.get_cmap('RdYlGn')
#     plt.scatter(x=range(len(data)), y=data, c=colours, cmap=cm, vmin=0, vmax=1)
#
#     plt.show()
