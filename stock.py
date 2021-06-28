from candle import Candle
from get_data import get_data
from optimize_levels import optimize_levels


class Stock:

    def __init__(self, ticker: str):
        self.period = '300d'
        self.ticker = ticker
        self.timeframes = ['1h', '1d', '1wk']
        self.charts = {}
        """
        Charts store daily candles, and lines
        - add moving averages and any other ideas for indicator creation
        """
        for timeframe in self.timeframes:
            self.charts[timeframe] = Chart(self.ticker, self.period, timeframe)

        """Obtain optimized levels"""
        # self.lines = optimize_levels(weekly, daily, hourly?)

    def ticker(self):
        return self.ticker

    def timeframes(self):
        return self.timeframes

    def price(self):
        return self.charts['1h'].current_price



class Chart:

    def __init__(self, ticker, period, timeframe):
        self.ticker = ticker
        self.period = period
        self.timeframe = timeframe
        self.data = self.getData()
        self.dates = self.data.index.tolist()
        self.opens = self.data['Open']
        self.closes = self.data['Close']
        self.highs = self.data['High']
        self.lows = self.data['Low']
        self.current_price = self.closes[-1]
        self.candles = []
        for i in range(len(self.dates)):
            self.candles.append(Candle(self.dates[i], self.opens[i], self.closes[i], self.highs[i], self.lows[i]))

        self.levels = self.getLevels()

        self.mavs = {}
        mav_n_s = [2, 7, 21, 35]
        mavs = self.getMAVs(mav_n_s)
        for i in range(len(mav_n_s)):
            self.mavs[mav_n_s[i]] = mavs[i]

    def getMAVs(self, n):
        y = []
        for mav in n:
            data = []
            for i in range(len(self.closes)):
                if i > mav:
                    data.append(sum([self.closes[z] for z in range(i-mav, i)]) / mav)
            y.append(data)
        return y

    def getLevels(self):

        """Look for two different chart patterns to define support/resistance"""
        # def isSupport(i):
        #     support = self.candles[i - 1].close - self.candles[i - 1].open < 0 and self.candles[i].close - self.candles[
        #         i].open >= 0
        #     return support
        #
        # def isResistance(i):
        #     resistance = self.candles[i - 1].close - self.candles[i - 1].open >= 0 and self.candles[i].close - \
        #                  self.candles[i].open < 0
        #     return resistance

        def isSupport(i):
            support = self.candles[i].close > self.candles[i-1].close and self.candles[i-1].open > self.candles[i].close
            return support
        def isResistance(i):
            resistance = self.candles[i].close < self.candles[i-1].close and self.candles[i-1].open < self.candles[i].close
            return resistance

        # def isSupport(i):
        #     support = self.candles[i].close > self.candles[i - 2].high \
        #               and self.candles[i - 2].close > self.candles[i - 1].close > self.candles[i - 2].open \
        #               or self.candles[i].low < self.candles[i - 1].low < self.candles[i - 2].low \
        #               and self.candles[i].low < self.candles[i + 1].low < self.candles[i + 2].low
        #     return support
        #
        # def isResistance(i):
        #     resistance = self.candles[i].close < self.candles[i - 1].close < self.candles[i - 2].close < self.candles[
        #         i - 1].close \
        #                  or self.candles[i].high > self.candles[i - 1].high > self.candles[i - 2].high \
        #                  and self.candles[i].high > self.candles[i + 1].high > self.candles[i + 2].high
        #     return resistance

        """
        Use getSup()/Res() to find levels in the chart
        store levels as { dates: price(level) }
        """
        levels = {}
        # +/- 2 range as isResistance/Support uses up to [+/- 2 indexing],
        # can probably reduce to 1 as only the commented out one needs 2
        for i in range(1, len(self.candles) - 1):
            if isSupport(i):
                if self.candles[i].open < self.candles[i - 1].close:
                    levels[self.candles[i].date] = self.candles[i].open
                else:
                    levels[self.candles[i - 1].date] = self.candles[i - 1].close
            elif isResistance(i):
                if self.candles[i].open > self.candles[i - 1].close:
                    levels[self.candles[i].date] = self.candles[i].open
                else:
                    levels[self.candles[i - 1].date] = self.candles[i - 1].close

        return levels

    def getData(self, timeframe=None):
        if timeframe == None:
            return get_data(self.ticker, self.period, self.timeframe).dropna()
        else:
            return get_data(self.ticker, self.period, timeframe).dropna()


    # def update_candles(self):
    #     count_new_candles = 0
    #     data = get_data(self.ticker, , self.interval_length)
    #     for i in range(len(data[0])):
    #         flag = False
    #         # flag = (candle is in self.candles)
    #         for j in range(len(self.candles)):
    #             if data[0][i] == self.candles[j].date:
    #                 flag = True
    #                 break
    #         if not flag:
    #             if data[2][i] > self.candles[-1]:
    #                 self.candles.append(Candle(data[0][i], data[1][i], data[2][i], data[3][i])
    #                 count_new_candles += 1
    #             else:
    #                 self.candles.append(Candle()
    #                 count_new_candles += 1
    #         if flag:
    #             pass
    #         return count_new_candles