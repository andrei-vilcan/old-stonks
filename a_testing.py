import matplotlib.pyplot as plt
from stock import Stock
from stock import savitzky_golay


stock = Stock('TSLA')

# fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
# ax1.plot(stock.charts['1d'].closes.tolist())
# ax2.plot(stock.charts['1d'].closes.tolist())
# ax3.plot(stock.charts['1d'].mav_dy[35])
# ax4.plot(stock.charts['1d'].mav_dy[21])
#
# ax3.axhline(y=0)
# ax4.axhline(y=0)
#
# for x in stock.charts['1d'].buy_n_sell_lines(35, 3)[0]:
#     ax1.axvline(x=x)
#
# for x in stock.charts['1d'].buy_n_sell_lines(11, 3)[1]:
#     ax2.axvline(x=x)
#
# plt.show()

fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(stock.charts['1d'].closes.tolist())
ax2.plot(stock.charts['1d'].closes.tolist())

hourly = stock.charts['1h'].derivative_scale_both()
daily = stock.charts['1d'].derivative_scale_both()
weekly = stock.charts['1wk'].derivative_scale_both()

data = []
for i in range(len(hourly)):
    d = 0
    w = 0
    data.append((hourly[i] + daily[d] + weekly[w]) / 3)
    if not i == 0:
        if i % 24 == 0:
            d += 1
        if i % 168 == 0:
            w += 1


ax3.plot(data)
# ax3.plot(stock.charts['1h'].derivative_scale_both())

# ax4.plot(stock.charts['1h'].mav_dy[35])
# ax5.plot(stock.charts['1h'].mav_ddy[35])
# ax4.axhline(y=0)
# ax5.axhline(y=0)

for x in stock.charts['1d'].buy_n_sell_lines(11, 1)[0]:
    ax1.axvline(x=x)

for x in stock.charts['1d'].buy_n_sell_lines(11, 1)[1]:
    ax2.axvline(x=x)

plt.show()
