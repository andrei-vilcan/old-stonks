import matplotlib.pyplot as plt
from stock import Stock
from stock import savitzky_golay


stock = Stock('CNI')

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(stock.charts['1h'].closes.tolist())
ax2.plot(stock.charts['1h'].closes.tolist())
# ax3.plot(stock.charts['1h'].horizontal_scale())
# ax4.plot(stock.charts['1h'].combined_scales())

for x in stock.charts['1h'].buy_n_sell_lines(9, 0.33)[0]:
    ax1.axvline(x=x)

for x in stock.charts['1h'].buy_n_sell_lines(9, 0.33)[1]:
    ax2.axvline(x=x)

plt.show()
 