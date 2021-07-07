import mplfinance as mpf
from stock import Stock
from optimize_levels import optimize_levels
import pandas as pd

"""Graph Kernel Density: can be used for relative strength indicator...
    true trend indicator may be of better use"""
# from scipy.stats import kde
# import matplotlib.pyplot as plt
# import numpy as np
# def k_density(stonk):
#     stock = Stock(stonk)
#     closes = list(stock.charts['1h'].closes)
#     kdensity = kde.gaussian_kde(closes, 0.9/len(closes))
#     xgrid = np.linspace(min(closes), max(closes))
#     plt.plot(xgrid, kdensity(xgrid))
#     plt.show()
#
# k_density('TSLA')


def graphData(stonk):
    stock = Stock(stonk)
    hourly_lines = optimize_levels(stock.charts['1h'])
    weekly_lines = optimize_levels(stock.charts['1wk'], hourly_lines)
    lines = list(weekly_lines.values())

    mpf.plot(stock.charts['1d'].getData(), mav=(7, 14), hlines=lines, type='candle', style='yahoo')

graphData("TSLA")
