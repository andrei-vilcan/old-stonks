import warnings
from candle import Candle
from get_data import get_data
from optimize_levels import optimize_levels
import numpy as np
import math as m
from math import factorial
mav_n_s = [5, 7, 11, 15, 21, 35, 49, 121]


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(int(window_size))
        order = np.abs(int(order))
    except ValueError as msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m_ = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    warnings.filterwarnings('ignore')
    firstvals = y[0] - np.abs(y [1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m_[::-1], y, mode='valid')


def chart_weight_formula(bias):
    # natural log
    x = m.log(bias)
    # linear
    # x = 2 * bias
    # quadratic
    # x = 0.7 * bias ** 2
    # exponential
    # x = 1.73 ** bias
    return x


class Stock:
    """
    Stock
    """
    ticker = str
    charts: dict

    def __init__(self, ticker: str, timeframes='1d'):
        self.ticker = ticker
        self.charts = {}
        if timeframes:
            if type(timeframes) == list:
                for timeframe in timeframes:
                    self.charts[timeframe] = Chart(self.ticker, timeframe)
            elif type(timeframes) == str:
                self.charts[timeframes] = Chart(self.ticker, timeframes)

    def ticker(self):
        return self.ticker.upper()

    def price(self):
        return self.charts.values()[-1].current_price


class Chart:

    def __init__(self, ticker, timeframe):
        self.ticker = ticker
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

        self.mav_y, self.mav_dy, self.mav_ddy = self.update_mavs()

    def getData(self):
        return get_data(self.ticker, self.timeframe)

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

        def isSupport(i):
            return self.candles[i - 1].close < self.candles[i].close < self.candles[i - 1].open
            # return self.candles[i].close > self.candles[i-1].close and self.candles[i-1].open > self.candles[i].close

        def isResistance(i):
            return self.candles[i - 1].close > self.candles[i].close > self.candles[i - 1].open
            # return self.candles[i].close < self.candles[i-1].close and self.candles[i-1].open < self.candles[i].close

        """
        Use getSup()/Res() to find levels in the chart
        store levels as { dates: price(level) }
        """
        levels = {}
        # +/- 2 range as isResistance/Support uses up to [+/- 2 indexing],
        # can probably reduce to 1 as only the commented out one needs 2
        for i in range(1, len(self.candles)):
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

    def update_mavs(self):
        y, dy, ddy = self.get_mavs(mav_n_s)
        mav_y = {}
        mav_dy = {}
        mav_ddy = {}
        for i in range(len(mav_n_s)):
            mav_y[mav_n_s[i]] = y[i]
            mav_dy[mav_n_s[i]] = dy[i]
            mav_ddy[mav_n_s[i]] = ddy[i]
        return mav_y, mav_dy, mav_ddy

    def get_mavs(self, mavs):
        y = []
        dy = []
        ddy = []
        for mav in mavs:
            y.append(savitzky_golay(self.closes, mav, 3))
            dy.append(savitzky_golay(self.closes, mav, 3, 1))
            ddy.append(savitzky_golay(self.closes, mav, 3, 2))
        return y, dy, ddy

    def buy_n_sell_lines(self, n, margin):
        buys = []
        sells = []
        for i in range(n, len(self.dates)):
            if 0 - margin <= self.mav_dy[n][i] <= 0 + margin:
                if self.mav_ddy[n][i] > 0:
                    buys.append(i)
                else:
                    sells.append(i)
        return buys, sells

    def derivative_scale(self):

        values = []
        max_cluster_count = 1

        clusters = self.cluster(self.buy_n_sell_lines(35, 3)[0])
        for i in range(35, len(self.closes)):
            for cluster_ in clusters:
                if i in range(min(cluster_), max(cluster_)):
                    strength = i - min(cluster_)
                    break
                else:
                    strength = 0

            if strength > max_cluster_count:
                max_cluster_count = strength

            factor = strength / max_cluster_count

            if i == 35:
                values.append(0.5 + (factor * 0.5))
            else:
                if strength == 0:
                    values.append(values[-1] - values[-1]/35)
                else:
                    values.append(values[-1] + factor)

        # values = savitzky_golay(values, 9, 3)

        return values

    # TODO

    def combined_scales(self):
        """n = mav"""
        scale = []
        horizontal_scale = self.horizontal_scale()
        ma_scale = self.ma_scale()
        for i in range(len(self.horizontal_scale())):
            scale.append(horizontal_scale[i] * 0.6 + 0.4 * ma_scale[i])
        """Smoothen scale maybe"""
        # scale = savitzky_golay(scale, 5, 3)
        return scale

    def optimized_levels(self):
        levels = optimize_levels(self)
        return levels

    def horizontal_scale(self):
        """
        Generate buy/sell scale for each candle based on distance from nearest horizontal
        support and resistance.

        TODO:
        - if passing resistance maintain sell pressure until price has confirmed the broken
            resistance as support
        """
        scale = []
        levels = optimize_levels(self)
        prices = list(levels.values())
        dates = list(levels.keys())
        for i in range(len(self.candles)):
            support = 0
            resistance = 0
            for n in range(len(levels)):
                if dates[n] < self.candles[i].date:
                    if prices[n] <= self.candles[i].close:
                        support = prices[n]
                    elif prices[n] > self.candles[i].close:
                        resistance = prices[n]
                        break
            if resistance == 0:
                if support == 0:
                    level = 0.5
                else:
                    level = (self.candles[i].close - support) / support
            else:
                level = (self.candles[i].close - support) / (resistance - support)
            scale.append(np.abs(level - 1))
        # smooth_scale = savitzky_golay(scale, 5, 3)
        return scale

    def ma_scale(self):
        scale = []
        for i in range(len(self.candles)):
            if all(i >= 0 for i in [self.mav_dy[15][i], self.mav_dy[35][i], self.mav_dy[49][i], self.mav_dy[121][i]]):
                scale.append(1)
            elif all(i >= 0 for i in [self.mav_dy[35][i], self.mav_dy[49][i], self.mav_dy[121][i]]):
                scale.append(0.5)
            elif all(i >= 0 for i in [self.mav_dy[49][i], self.mav_dy[121][i]]):
                scale.append(0.25)
            else:
                scale.append(0)
        # scale = savitzky_golay(np.array(scale), 5, 3)
        return scale

    def evaluate(self):
        return [1]

    def cluster(self, gap=1.02):
        # lines: list of indexes of significant points
        line_clusters = []

        # Iter through initial lines
        for i in self.buy_n_sell_lines(35, 3)[0]:
            count = 0
            # if first iter, create new cluster
            if count == 0:
                line_clusters.append([i])
                count += 1
            else:
                # get max/min/median of current group
                current_group = line_clusters[-1]
                prices = float(np.average([x[1] for x in current_group]))

                # if price is within max/min * median of group, add to group
                if i / line_clusters[-1][-1] > gap:
                    line_clusters[-1].append(i)
                else:
                    # create new group
                    line_clusters.append([i])
        group_prices = [sum(x)/len(x) for x in line_clusters]
        return line_clusters

    def default_weight(self, bias):
        if self.ticker == '1h':
            weight = 1 + bias
        elif self.ticker == '1d':
            weight = 24 + bias
        elif self.ticker == '1wk':
            weight = 168 + bias
        else:
            weight = 0
        return weight