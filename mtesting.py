import matplotlib.pyplot as plt
from stock import Stock

stock = Stock('NVDA')
data = list(stock.charts['1d'].closes)[21:]
colours = stock.charts['1d'].combined_scales(21)

"""Setup MAV for Graph"""
# add blank zeros to fill in missing points in moving average
def create_mav(n):
    mav = stock.charts['1d'].mav_y[n]
    return mav


# first_dev_35 = stock.charts['1d'].mav_dy[35]
# first_dev_14 = stock.charts['1d'].mav_dy[14]
# first_dev_7 = stock.charts['1d'].mav_dy[7]
#
# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.plot(data)
# ax2.plot(first_dev_35)
# ax3.plot(first_dev_14)

cm = plt.cm.get_cmap('coolwarm')
plt.scatter(x=range(len(data)), y=data, c=colours, cmap=cm)

#
# for point in stock.charts['1d'].buy_lines(7)[0]:
#     ax1.axvline(x=point)

plt.show()