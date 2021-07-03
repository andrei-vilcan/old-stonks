from candle import Candle
from get_data import get_data
from optimize_levels import optimize_levels
import numpy as np
import math as m
from math import factorial


def cluster(lines, mingap=0.95, maxgap=1.05):
    groups = []
    inGroup = False

    # Iter through initial lines
    for i in range(len(lines)):

        line = lines[i]
        # if first iter, create new cluster
        if i == 0:
            groups.append([i])
        else:
            # get max/min/median of current group
            current_group = groups[-1]
            max_ = max(current_group)
            min_ = min(current_group)
            median_ = (max_ + min_) / 2
            # if price is within max/min * median of group, add to group
            if median_ * maxgap > line > median_ * mingap:
                groups[-1].append(i)
            else:
                # create new group
                groups.append([line])

    return groups


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError as msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve(m[::-1], y, mode='valid')


mav_n_s = [5, 7, 11, 21, 35]


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

    def __init__(self, ticker: str):
        self.period = '370d'
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

    def charts(self, time_frame):
        # if time_frame:
        #     return self.charts
        # else:
        if time_frame == '1h':
            return self.charts['1d']
        if time_frame == '1d':
            return self.charts['1d']
        elif time_frame == '1wk':
            return self.charts['1wk']

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

        self.mav_y, self.mav_dy, self.mav_ddy = self.update_mavs()

    def getData(self, timeframe=None):
        if not timeframe:
            return get_data(self.ticker, self.period, self.timeframe)
        else:
            return get_data(self.ticker, self.period, timeframe).dropna()

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
        for i in range(n, len(self.closes)):
            if 0 - margin <= self.mav_dy[n][i] <= 0 + margin:
                if self.mav_ddy[n][i] > 0:
                    buys.append(i)
                else:
                    sells.append(i)
        return buys, sells

    def derivative_scale_primitive(self):
        values = []
        
        buys = self.buy_n_sell_lines(35, 3)[0]
        sells = self.buy_n_sell_lines(35, 3)[1]

        for i in range(len(self.closes)):
            # shiii
            pass

    def derivative_scale(self):

        values = []
        max_cluster_count = 1

        clusters = cluster(self.buy_n_sell_lines(35, 3)[0])
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

        values = savitzky_golay(values, 9, 3)

        return values

    def derivative_scale_both(self):

        values = []
        max_buy_cluster_count = 1
        max_sell_cluster_count = 1

        buy_clusters = cluster(self.buy_n_sell_lines(35, 3)[0])
        sell_clusters = cluster(self.buy_n_sell_lines(35, 3)[1])
        for i in range(35, len(self.closes)):

            for cluster_ in buy_clusters:
                if i in range(min(cluster_), max(cluster_)):
                    buy_strength = i - min(cluster_)
                    break
                else:
                    buy_strength = 0

            if buy_strength > max_buy_cluster_count:
                max_buy_cluster_count = buy_strength

            for cluster_ in sell_clusters:
                if i in range(min(cluster_), max(cluster_)):
                    sell_strength = - (i - min(cluster_))
                    break
                else:
                    sell_strength = 0

            if sell_strength < max_sell_cluster_count:
                max_sell_cluster_count = sell_strength

            ovr_strength = buy_strength + sell_strength

            if ovr_strength > 0:
                factor = ovr_strength / max_buy_cluster_count
            elif ovr_strength < 0:
                factor = ovr_strength / max_buy_cluster_count
            else:
                factor = 0

            if i == 35:
                values.append(0.5 + factor)
            else:
                values.append(values[-1] + factor)

        # values = savitzky_golay(values, 35, 3)

        return values

    # TODO
    def combined_scales(self, n):
        """n = mav"""
        scale = []
        for i in range(len(self.ma_scale(n))):
            scale.append(1.5 * self.horizontal_scale()[i] + 0.5 * self.ma_scale(n)[i])

        """Smoothen scale maybe"""
        return scale

    def horizontal_scale(self):
        """Matt's method"""
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
            level = (self.candles[i].close - support) / (resistance - support)
            scale.append(level)
            smooth_scale = savitzky_golay(scale, 31, 4)
        return smooth_scale

    def ma_scale(self, n):
        ma = self.mav_y[n]
        scale = []
        for i in range(n, len(self.candles)):
            value = (self.candles[i].close - ma[i]) / self.candles[i].close
            scale.append(value)
        return scale

    def evaluate(self):
        return [1]

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

# s = Stock('TSLA')
# print(s.derivative_scale())
