from stock import Stock
import matplotlib.pyplot as plt
from reddit_scraper import tickers
from optimize_levels import optimize_levels

stonks = []

"""Remove '$' from tickers, add to stocks"""
for k,v in tickers.items():
    if v > 4 and '$' in str(k):
        stonks.append(k.replace('$',''))


setups = []
"""Iterate through stocks and find colour values (store in setups)"""
for stonk in stonks:
    try:
        """Define Parameters"""
        stock = Stock(stonk)
        chart = stock.charts['1d']
        closes = list(chart.closes)
        colours = chart.horizontal_scale()

        lines = []
        [lines.append(line) for line in optimize_levels(chart).values() if line not in lines]

        """
        Iterate through stocks (from present to past), find a 'set up' 
        a set up being once a stock has moved above resistance and is coming 
        back into it to test it as support
        """
        current_price = closes[-1]
        setups.append((stock, colours[-1]))
    except:
        pass
"""sort setups from small to large to find best buy"""
setups = sorted(setups, key=lambda x: x[1])

"""print stonks w scale"""
cm = plt.cm.get_cmap('RdYlGn')
for setup in setups[:5]:
    plt.scatter(x=range(len(setup[0].charts['1d'].closes)), y=setup[0].charts['1d'].closes, c=setup[0].charts['1d'].horizontal_scale())