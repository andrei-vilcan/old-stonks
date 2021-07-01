import matplotlib.pyplot as plt
from stock import Stock

stock = Stock('TSLA')

data = list(stock.charts['1d'].closes)


# """Setup MAV for Graph"""
# add blank zeros to fill in missing points in moving average
# def create_mav(n):
#     mav = stock.charts['1d'].mav_y[n]
#     return mav

# """Setup First derivative for graph"""
# def get_first_derivative(mav):
#     mav_first_derivative = []
#     for i, val in enumerate(mav):
#         if i > 0:
#             mav_first_derivative.append(mav[i] - mav[i - 1])
#     # zeros.extend(mav_first_derivative)
#     return mav_first_derivative

# """Find first derivative == 0, e.g. indexes when first dev goes from -ve to +ve"""
# def get_zeros(mavs: list):
#     inPositive = False
#     points = []
#     # index one of the mav's data
#     for i in range(len(mavs[0])):
#         if mavs[0][i] > 0 and mavs[1][i] > 0 and mavs[2][i] > 0:
#             if not inPositive:
#                 inPositive = True
#                 points.append(i)
#         else:
#             if inPositive:
#                 inPositive = False
#                 # sell point perhaps
#     return points


# first_dev_7 = stock.charts['1d'].mav_dy[7]
# first_dev_14 = stock.charts['1d'].mav_dy[14]
# first_dev_35 = stock.charts['1d'].mav_dy[35]
#
# fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
# ax1.plot(data)
# ax2.plot(data)
# ax3.plot(first_dev_7)
# ax4.plot(first_dev_14)
#
# ax3.axhline(y=0)
# ax4.axhline(y=0)
#
# for x in stock.charts['1d'].buy_lines(2, 5)[0]:
#     ax1.axvline(x=x)
#
# for x in stock.charts['1d'].buy_lines(2, 3)[1]:
#     ax2.axvline(x=x)
#
# plt.show()


def simulate(a_stock: Stock):
    money_owned = 1000
    stock_owned = 0

    buy_amount = 50
    sell_amount = 75

    buys = a_stock.charts['1d'].buy_n_sell_lines(7, 0.3)[0]
    sells = a_stock.charts['1d'].buy_n_sell_lines(2, 0.05)[1]
    for i in range(75, len(a_stock.charts['1d'].candles)):
        if i in buys:
            assert money_owned > 0
            money_owned += -buy_amount
            stock_owned += buy_amount / a_stock.charts['1d'].candles[i].close
        if i in sells:
            stock_owned += - sell_amount / a_stock.charts['1d'].candles[i].close
            money_owned += sell_amount
        if i == len(a_stock.charts['1d'].candles) - 1:
            money_owned += stock_owned * a_stock.charts['1d'].candles[i].close

    return money_owned


print(simulate(stock))
