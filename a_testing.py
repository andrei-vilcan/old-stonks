import matplotlib.pyplot as plt
from stock import Stock
from stock import savitzky_golay


stock = Stock('CNI')

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
ax1.plot(stock.charts['1d'].closes.tolist())
ax2.plot(stock.charts['1d'].ma_scale())
ax3.plot(stock.charts['1d'].horizontal_scale())
ax4.plot(stock.charts['1d'].combined_scales())

for x in stock.charts['1d'].buy_n_sell_lines(11, 0.5)[0]:
    ax1.axvline(x=x)


plt.show()
