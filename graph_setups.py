from stock import Stock
# # from reddit_scraper import tickers_letters_only
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
cm = plt.cm.get_cmap('RdYlGn')


"""Graph Tickers and Plot Setups"""
tickers = ['btc-usd', 'eth-usd', 'ada-usd', 'xlm-usd', 'bnb-usd', 'eos-usd', 'bch-usd', 'hex-usd', 'doge-usd', 'aave-usd']
# tickers = ['hex-usd']
# tickers = ['tsla', 'amd', 'nvda', 'aapl', 'msft', 'cni', 'ko', 'amc', 'crsp', 'spce', 'sq', 'pypl', 'pins']


for ticker in tickers:
    try:
        stock = Stock(ticker, '30m')
        prices = list(stock.charts['30m'].closes)
        colours = list(stock.charts['30m'].combined_scales())
        trades = []
        # Moving average of colours
        c_ma = []
        for i in range(len(colours)):
            if i == 0:
                c_ma.append(colours[i])
            elif i == 1:
                c_ma.append(sum(colours[:2])/ 2)
            elif i == 2:
                c_ma.append(sum(colours[:3]) / 3)
            else:
                c_ma.append(sum(colours[i-3:i+1]) / 4)
            # else:
            #     c_ma.append(sum(colours[i-4:i+1]) / 5)
        # Variables to monitor trades
        inTrade = False
        entry_point = 0
        exit_point = 0
        # Graph coloured chart
        fig, (ax1) = plt.subplots(1)
        ax1.scatter(x=range(len(prices)), y=prices, c=colours, cmap=cm)
        # ax2.plot(c_derivative)
        # Graph trades
        for i in range(len(prices)):
            if not inTrade:
                # Enter trade if green enough, record entry price
                if colours[i] >= 0.775:
                    entry_point = prices[i]
                    ax1.axvline(x=i, color='g')
                    inTrade = True
            elif inTrade:
                # Exit trade if red enough
                if colours[i] <= 0.275:
                    exit_point = prices[i]
                    inTrade = False
                    ax1.axvline(x=i, color='r')
                    plt.text(x=i, y=prices[i], s=str(100 * (exit_point - entry_point) / entry_point)[:4] + '%')
                    trades.append(100 * (exit_point - entry_point) / entry_point)
        # Graph Resistance/Support
        dates = stock.charts['30m'].dates
        for date, level in stock.charts['30m'].optimized_levels().items():
            ax1.hlines(y=level, xmin=dates.index(date), xmax=len(prices))
        # Add date labels
        print(np.average(trades))
        plt.show()

    except Exception as e:
        print(e)
        pass


# """Graph Horizontal Lines"""
# stonks = ['TSLA']
# for stock in stonks:
#     stock = Stock(stock)
#     prices = list(stock.chart.closes)
#     colours = list(stock.chart.combined_scales())
#     plt.scatter(x=range(len(prices)), y=prices, c=colours, cmap=cm)
#     for date, level in stock.chart.optimized_levels().items():
#         dates = stock.chart.dates
#         plt.hlines(y=level, xmin=dates.index(date), xmax=len(prices))
#     plt.show()