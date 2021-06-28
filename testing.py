import matplotlib.pyplot as plt
from stock import Stock

stock = Stock('TSLA')
data = list(stock.charts['1h'].closes)

plt.figure(figsize=(8,8))
fig, axs = plt.subplots(2)
axs[0].plot(data)
# axs[1].plot(
#     [0 for n in range(7)].extend(stock.charts['1d'].mavs[7])
# )
plt.show()