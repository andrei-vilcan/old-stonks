from stock import savitzky_golay
from candle import Candle
from get_data import get_data
from optimize_levels import optimize_levels
import numpy as np
import math as m
from math import factorial
from typing import List
import heapq

mav_n_s = [7, 11, 17, 25, 39]


class AlgoChart:

    def __init__(self, data):
        self.ticker = data[0]
        self.period = data[1]
        self.timeframe = data[2]

        self.dates = data[3].index.tolist()
        self.opens = data[4]['Open']
        self.closes = data[5]['Close']
        self.highs = data[6]['High']
        self.lows = data[7]['Low']
        self.current_price = self.closes[-1]

        self.candles = []
        for i in range(len(self.dates)):
            self.candles.append(Candle(self.dates[i], self.opens[i], self.closes[i], self.highs[i], self.lows[i]))

        self.levels = self.getLevels()

        self.mav_y = {}
        self.mav_dy = {}
        self.mav_ddy = {}
        self.update_mavs()

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

    def update_mavs(self):
        y, dy, ddy = self.get_mavs(mav_n_s)
        for i in range(len(mav_n_s)):
            self.mav_y[mav_n_s[i]] = y[i]
            self.mav_dy[mav_n_s[i]] = dy[i]
            self.mav_ddy[mav_n_s[i]] = ddy[i]

    def get_mavs(self, n):
        y = []
        dy = []
        ddy = []
        # for mav in n:
        #     # moving average for each day
        #     moving_average = []
        #     for i in range(len(self.closes)):
        #         if i >= mav - 1:
        #             moving_average.append(sum([self.closes[z] for z in range(i - mav + 1, i + 1)]) / mav)
        #         else:
        #             moving_average.append(0)
        #
        #     slopes_1 = []
        #     for i in range(len(moving_average)):
        #         if i >= mav:
        #             slopes_1.append(moving_average[i] - moving_average[i - 1])
        #         else:
        #             slopes_1.append(0)
        #
        #     # first derivatives
        #     first = []
        #     for i in range(len(slopes_1)):
        #         if i >= mav + 1:
        #             if i == len(slopes_1) - 1:
        #                 first.append(slopes_1[i])
        #             else:
        #                 first.append((slopes_1[i] + slopes_1[i - 1]) / 2)
        #         else:
        #             first.append(0)
        #
        #     slopes_2 = []
        #     for i in range(1, len(first)):
        #         if i >= mav + 1:
        #             slopes_2.append(first[i] - first[i - 1])
        #         else:
        #             slopes_2.append(0)
        #
        #     # second derivatives
        #     second = []
        #     for i in range(len(slopes_2)):
        #         if i >= mav + 2:
        #             if i == len(slopes_2) - 1:
        #                 second.append(slopes_2[i])
        #             else:
        #                 second.append((slopes_2[i] + slopes_2[i - 1] / 2))
        #         else:
        #             second.append(0)
        #
        #     y.append(moving_average)
        #     dy.append(first)
        #     ddy.append(second)
        for mav in n:
            y.append(savitzky_golay(self.closes, mav + 4, 4))
            dy.append(savitzky_golay(self.closes, mav + 4, 4, 1))
            ddy.append(savitzky_golay(self.closes, mav + 4, 4, 2))

        return y, dy, ddy

    def buy_n_sell_lines(self, n, margin):
        buy = []
        sell = []
        for i in range(n + 4, len(self.dates) - 1):
            # if flat
            if 0 - margin <= self.mav_dy[n][i] <= 0 + margin:
                # if up
                if self.mav_ddy[n][i] > 0:
                    buy.append(i)
                else:
                    sell.append(i)
        return buy, sell

    def derivative_scale(self):
        buys = self.buy_n_sell_lines(11, 0.5)[0]
        sells = self.buy_n_sell_lines(7, 0.1)[1]

        values = []
        for i in range(len(self.closes)):
            if i in buys:
                values.append(3)
            elif i in sells:
                values.append(1)
            else:
                values.append(2)

        return savitzky_golay(values, 11, 4)

    # TODO
    def combined_scales(self, n):
        """n = mav"""
        scale = []
        for i in range(len(self.ma_scale(n))):
            scale.append(1.5 * self.horizontal_scale()[i] + 0.5 * self.ma_scale(n)[i])

        """Smoothen scale"""
        smooth_scale = savitzky_golay(scale, 31, 4)
        return smooth_scale

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
