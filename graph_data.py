import mplfinance as mpf
from stock import Stock, Chart
from optimize_levels import optimize_levels

"""Graph Kernel Density: can be used for relative strength indicator...
    true trend indicator may be of better use"""
# from scipy.stats import kde
# import matplotlib.pyplot as plt
# import numpy as np

#
# def k_density(stonk):
#     stock = Stock(stonk)
#     closes = list(stock.charts['1h'].closes)
#     kdensity = kde.gaussian_kde(closes, 0.9/len(closes))
#     xgrid = np.linspace(min(closes), max(closes))
#     plt.plot(xgrid, kdensity(xgrid))
#     plt.show()
#
#
# k_density('TSLA')


def graphData(stonk):
    stock = Stock(stonk)
    weekly_lines = optimize_levels(stock.charts['1wk'])
    daily_lines = optimize_levels(stock.charts['1d'], weekly_lines)
    hourly_lines = optimize_levels(stock.charts['1h'], weekly_lines)
    lines = list(hourly_lines.values())

    mpf.plot(stock.charts['1d'].getData(), mav=(2, 7, 21, 35), hlines=lines, type='candle', style='yahoo')


graphData('CNI')

#
# def colour_meter(chart: Chart) -> [float]:
#     slopes = []
#     for day in range(1, len(chart.dates)):
#         slope = chart.closes[day] - chart.closes[day - 1]
#         slopes.append(slope)
#     min_slope, max_slope = min(slopes), max(slopes)
