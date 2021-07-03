import matplotlib.pyplot as plt
from stock import Stock

mav = 21

stock = Stock('LGIQ')
data = list(stock.charts['1d'].closes)[11:]
colours = stock.charts['1d'].combined_scales(11)


cm = plt.cm.get_cmap('RdYlGn')
plt.scatter(x=range(len(data)), y=data, c=colours, cmap=cm)
# for point in buys:
#     plt.axvline(x=point)

plt.show()
