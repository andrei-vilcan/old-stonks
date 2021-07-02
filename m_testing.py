import matplotlib.pyplot as plt
from stock import Stock

mav = 21

stock = Stock('AAPL')
data = list(stock.charts['1d'].closes)
colours = stock.charts['1d'].horizontal_scale()

buys = stock.charts['1d'].buy_n_sell_lines(7, 0.3)[0]
sells = stock.charts['1d'].buy_n_sell_lines(2, 0.05)[1]

# first_dev_35 = stock.charts['1d'].mav_dy[35]
# first_dev_14 = stock.charts['1d'].mav_dy[14]
# first_dev_7 = stock.charts['1d'].mav_dy[7]
#
# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.plot(data)
# ax2.plot(first_dev_35)
# ax3.plot(first_dev_14)

cm = plt.cm.get_cmap('RdYlGn')
plt.scatter(x=range(len(data)), y=data, c=colours, cmap=cm)


for point in buys:
    plt.axvline(x=point)

plt.show()