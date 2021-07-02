import matplotlib.pyplot as plt
from stock import Stock
from stock import savitzky_golay

stock = Stock('TSLA')

# data = list(stock.charts['1d'].closes)


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

#
# def simulate(a_stock: Stock):
#     money_owned = 1000
#     stock_owned = 0
#
#     buy_amount = 50
#     sell_amount = 75
#
#     buys = a_stock.charts['1d'].buy_n_sell_lines(11, 0.5)[0]
#     sells = a_stock.charts['1d'].buy_n_sell_lines(7, 0.1)[1]
#     for i in range(75, len(a_stock.charts['1d'].candles)):
#         if i + 2 in buys:
#             # assert money_owned > 0
#             money_owned += -buy_amount
#             stock_owned += buy_amount / a_stock.charts['1d'].candles[i].close
#         if i + 2 in sells:
#             stock_owned += - sell_amount / a_stock.charts['1d'].candles[i].close
#             money_owned += sell_amount
#         if i + 2 == len(a_stock.charts['1d'].candles) - 1:
#             money_owned += stock_owned * a_stock.charts['1d'].candles[i].close
#
#     return money_owned
#
#
# tesla = Stock('TSLA')
# apple = Stock('AAPL')
# microsoft = Stock('MSFT')
# nvidia = Stock('NVDA')
# qualcomm = Stock('QCOM')
# cni = Stock('CNI')
#
# stocks = [tesla, apple, microsoft, nvidia, qualcomm, cni]
#
# count = 0
# growth = 0
# for stock in stocks:
#     count += 1
#     growth += simulate(stock)
# print(growth/count)

fig, (ax1) = plt.subplots(1)
ax1.plot(stock.charts['1d'].derivative_scale())

plt.show()
