import mplfinance as mpf
import datetime
from candle import Candle
from get_data import get_data

all_stocks = []

def add_stock(ticker: str, intervals: [str]):
    all_stocks.append(Stock(ticker, intervals))

class Stock:

    def __init__(self, ticker: str):
        self.period = '180d'
        self.ticker = ticker
        self.timeframes = ['1wk', '1d', '1mo', '1h']
        self.charts = {}
        for timeframe in self.timeframes:
            self.charts[timeframe] = Chart(self.ticker, self.period, timeframe)

    def ticker(self):
        return self.ticker

    def timeframes(self):
        return self.timeframes




class Chart:


    def __init__(self, ticker, period, timeframe):
        self.ticker = ticker
        self.period = period
        self.timeframe = timeframe
        self.data = get_data(self.ticker, self.period, self.timeframe).dropna()
        self.candles = []
        dates = self.data.index.tolist()
        opens = self.data['Open']
        closes = self.data['Close']
        highs = self.data['High']
        lows = self.data['Close']
        for i in range(len(dates)):
            self.candles.append(Candle(dates[i], opens[i], closes[i], highs[i], lows[i]))


    def getLevels(self):
        def isSupport(i):
            support = self.candles[i].close > self.candles[i - 2].high \
                      and self.candles[i - 2].close > self.candles[i - 1].close > self.candles[i - 2].open \
                      or self.candles[i].low < self.candles[i - 1].low < self.candles[i - 2].low \
                      and self.candles[i].low < self.candles[i + 1].low < self.candles[i + 2].low
            return support

        def isResistance(i):
            resistance = self.candles[i].close < self.candles[i - 1].close < self.candles[i - 2].close < self.candles[i - 1].close \
                         or self.candles[i].high > self.candles[i - 1].high > self.candles[i - 2].high \
                         and self.candles[i].high > self.candles[i + 1].high > self.candles[i + 2].high
            return resistance

        def cluster(levels):
            groups = []
            dates = [d for d in levels.keys()]
            prices = [p for p in levels.values()]
            for date, price in zip(dates, prices):
                i = dates.index(date)
                if i == 0:
                    groups.append([price])
                else:
                    maxgap = 0.1
                    if abs(price - (max(groups[-1]) + min(groups[-1]))/2)/price <= maxgap:
                        groups[-1].append(price)
                    else:
                        groups.append([price])
            return groups

        levels = {}
        for i in range(2, len(self.candles) - 2):
            if isSupport(i):
                levels[self.candles[i].date] = self.candles[i - 1].close
            elif isResistance(i):
                if self.candles[i].open > self.candles[i - 1].close:
                    levels[self.candles[i].date] = self.candles[i].open
                else:
                    levels[self.candles[i - 1].date] = self.candles[i - 1].close

        clustered_levels = cluster(levels)
        refined_levels = [max(cluster) for cluster in clustered_levels]

        for cluster in clustered_levels:
            refined_levels.append(min(cluster))
        # for close in Stock(self.ticker).charts['1mo'].closes:
        #     refined_levels.append(close) ##

        return refined_levels