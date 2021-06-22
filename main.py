import matplotlib.pyplot as plt
from matplotlib import cm
from stock import Stock
from getsupportresistance import getLevels

add_stock('AAPL', '1d')


res = getLevels(Stock('VSQTF', '1d'))


plt.figure(figsize=(12.5,8.5))
plt.style.use('seaborn-whitegrid')
twilight = cm.get_cmap('twilight')

n, bins, patches = plt.hist(res, bins=max(res)-min(res)/2, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7)
n = n.astype('int')
for i in range(len(patches)):
    patches[i].set_facecolor(plt.cm.twilight(n[i] / max(n)))

plt.show()