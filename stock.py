from candle import Candle
from get_data import get_data

import matplotlib.pyplot as plt


class Stock:

    def __init__(self, ticker: str):
        self.period = '300d'
        self.ticker = ticker
        self.charts = {}
        """
        Charts store daily candles, and lines
        - add moving averages and any other ideas for indicator creation
        """
        for timeframe in ['1h', '1d', '1wk']:
            self.charts[timeframe] = Chart(self.ticker, self.period, timeframe)

        """Obtain optimized levels"""
        # self.lines = optimize_levels(weekly, daily, hourly?)

    def ticker(self):
        return self.ticker

    def charts(self):
        return self.charts

    # TODO
    def update(self):
        for chart in self.charts.values:
            chart.update()

    def add_time_frame(self, time_frame_s):
        if time_frame_s.isinstance(str):
            self.charts[time_frame_s] = Chart(self.ticker, self.period, time_frame_s)
        else:
            for thing in time_frame_s:
                self.charts[thing] = Chart(self.ticker, self.period, thing)

    def price(self):
        return self.charts['1h'].current_price


class Chart:

    def __init__(self, ticker, period, timeframe):
        self.ticker = ticker
        self.period = period
        self.timeframe = timeframe

        data = self.getData()
        self.dates = data.index.tolist()
        self.opens = data['Open']
        self.closes = data['Close']
        self.highs = data['High']
        self.lows = data['Low']
        self.current_price = self.closes[-1]

        self.candles = []
        for i in range(len(self.dates)):
            self.candles.append(Candle(self.dates[i], self.opens[i], self.closes[i], self.highs[i], self.lows[i]))

        self.levels = self.getLevels()

        self.mav_y = {}
        self.mav_dy = {}
        self.mav_ddy = {}
        self.update_mavs()

    # TODO
    def update(self):
        pass


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

    def update_mavs(self):
        mav_n_s = [2, 7, 14, 21, 35]
        y, dy, ddy = self.get_mavs(mav_n_s)
        for i in range(len(mav_n_s)):
            self.mav_y[mav_n_s[i]] = y[i]
            self.mav_dy[mav_n_s[i]] = dy[i]
            self.mav_ddy[mav_n_s[i]] = ddy[i]

    def get_mavs(self, n):
        y = []
        dy = []
        ddy = []
        for mav in n:
            # moving average for each day
            moving_average = []
            for i in range(len(self.closes)):
                if i >= mav - 1:
                    moving_average.append(sum([self.closes[z] for z in range(i - mav + 1, i + 1)]) / mav)
                else:
                    moving_average.append(0)

            slopes_1 = []
            for i in range(len(moving_average)):
                if i >= mav:
                    slopes_1.append(moving_average[i] - moving_average[i - 1])
                else:
                    slopes_1.append(0)

            # first derivatives
            first = []
            for i in range(len(slopes_1)):
                if i >= mav + 1:
                    if i == len(slopes_1) - 1:
                        first.append(slopes_1[i])
                    else:
                        first.append((slopes_1[i] + slopes_1[i - 1]) / 2)
                else:
                    first.append(0)

            slopes_2 = []
            for i in range(1, len(first)):
                if i >= mav + 1:
                    slopes_2.append(first[i] - first[i - 1])
                else:
                    slopes_2.append(0)

            # second derivatives
            second = []
            for i in range(len(slopes_2)):
                if i >= mav + 2:
                    if i == len(slopes_2) - 1:
                        second.append(slopes_2[i])
                    else:
                        second.append((slopes_2[i] + slopes_2[i - 1] / 2))
                else:
                    second.append(0)

            y.append(moving_average)
            dy.append(first)
            ddy.append(second)

        return y, dy, ddy

    # TODO
    # def buy_sell_scale(self) -> [float]:

    def buy_lines(self, n):
        buy = []
        sell = []
        margin = 0.2
        for i in range(n, len(self.dates)):
            # if flat
            if 0 - margin <= self.mav_dy[n][i] <= 0 + margin:
                # if up
                if self.mav_ddy[n][i] > 0:
                    buy.append(i)
                else:
                    sell.append(i)
        return buy, sell

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
            return self.candles[i - 1].close < self.candles[i].close < self.candles[i - 1].open
            # return self.candles[i].close > self.candles[i-1].close and self.candles[i-1].open > self.candles[i].close

        def isResistance(i):
            return self.candles[i - 1].close > self.candles[i].close > self.candles[i - 1].open
            # return self.candles[i].close < self.candles[i-1].close and self.candles[i-1].open < self.candles[i].close

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
        if timeframe is None:
            return get_data(self.ticker, self.period, self.timeframe).dropna()
        else:
            return get_data(self.ticker, self.period, timeframe).dropna()

#
# nvidia = Stock('NVDA')
# tesla = Stock('TSLA')
#
# y = list(tesla.charts['1d'].closes)
# x = [i for i in range(len(y))]


