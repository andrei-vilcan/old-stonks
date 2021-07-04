import matplotlib.pyplot as plt
from stock import Stock
from optimize_levels import optimize_levels


stock = Stock('SPCE')
data = list(stock.charts['1d'].closes)
colours = stock.charts['1d'].combined_scales()


cm = plt.cm.get_cmap('RdYlGn')
plt.scatter(x=range(len(data)), y=data, c=colours, cmap=cm)
# for point in (get h lines):
#     plt.axhline(y=point)

plt.show()
