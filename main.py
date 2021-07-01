from stock import Stock
from graph_data import graphData
from ticker_scrapers.reddit_scraper import tickers

stocks = []

"""Remove '$' from tickers, add to stocks"""
for k,v in tickers.items():
    if v > 4 and '$' in str(k):
        stocks.append(k.replace('$',''))

setups = []

"""Iterate through stocks and find best entries (setups)"""
for stonk in stocks:
    try:
        """Define Stocks"""
        stock = Stock(stonk)
        chart = stock.charts['1d']
        closes = chart.closes.tolist()
        lines = []
        [lines.append(line) for line in stock.charts['1h'].optimized_levels if line not in lines].sort()

        """
        Iterate through stocks (from present to past), find a 'set up' 
        a set up being once a stock has moved above resistance and is coming 
        back into it to test it as support
        """
        current_price = closes[-1]

        for i in range(1, len(lines)):
            if lines[-i] < current_price:
                support = lines[-i]
                if any(close > current_price for close in closes[-3:]):
                    setups.append((stock.ticker, float(current_price / lines[-i])))
                    break
    except:
        pass

for setup in setups:
    graphData(setup[0])