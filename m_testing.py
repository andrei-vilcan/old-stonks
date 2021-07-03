import matplotlib.pyplot as plt
from stock import Stock
from optimize_levels import optimize_levels

mav = 21

stock = Stock('cni')
data = list(stock.charts['1d'].closes)
colours = stock.charts['1d'].combined_scales()


cm = plt.cm.get_cmap('RdYlGn')
plt.scatter(x=range(len(data)), y=data, c=colours, cmap=cm)
plt.plot(stock.charts['1d'].mav_y[121], 'r')
plt.plot(stock.charts['1d'].mav_y[49], 'g')
plt.plot(stock.charts['1d'].mav_y[35], 'b')
# for point in buys:
#     plt.axvline(x=point)

plt.show()
