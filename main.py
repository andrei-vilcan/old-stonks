from stock import Stock
import matplotlib.pyplot as plt
from reddit_scraper import tickers

stonks = []

"""Remove '$' from tickers, add to stocks"""
for k,v in tickers.items():
    if v > 1 and '$' in str(k):
        stonks.append(k.replace('$',''))
# stonks = {k: v for k, v in sorted(tickers.items(), key=lambda item: item[1], reversed=True)} if stonk is dic

stonk_ratings = {}

"""Iterate through stocks and find values for buy/sell signal"""
for stonk in stonks:
    try:
        """Define Parameters"""
        stock = Stock(stonk)
        colours = stock.charts['1d'].combined_scales()
        """
        Iterate through stocks (from present to past), find a 'set up' 
        a set up being once a stock has moved above resistance and is coming 
        back into it to test it as support
        """
        stonk_ratings[stock.ticker] = colours[-1]
    except:
        pass

"""sort setups from small to large to find best buy"""
buys = {k: v for k, v in sorted(stonk_ratings.items(), key=lambda item: item[1])}

"""print stonks w scale"""
cm = plt.cm.get_cmap('RdYlGn')
fig, ax = plt.subplots(3)
iter = 0
for stonk in list(buys.keys())[-3:]:
    stock = Stock(stonk)
    closes = list(stock.charts['1d'].closes)
    colours = stock.charts['1d'].combined_scales()
    ax[iter].scatter(x=range(len(closes)), y=closes, c=colours, cmap=cm)
    iter += 1
plt.show()