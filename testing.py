import matplotlib.pyplot as plt
from stock import Stock

stock = Stock('TSLA')
data = list(stock.charts['1d'].closes)


"""Setup MAV for Graph"""
# add blank zeros to fill in missing points in moving average
def create_mav(n):
    mav = stock.charts['1d'].mav_y[n]
    return mav


# """Setup First derivative for graph"""
# def get_first_derivative(mav):
#     mav_first_derivative = []
#     for i, val in enumerate(mav):
#         if i > 0:
#             mav_first_derivative.append(mav[i] - mav[i - 1])
#     # zeros.extend(mav_first_derivative)
#     return mav_first_derivative


# """Find first derivative == 0, e.g. indexes when first dev goes from -ve to +ve"""
# def get_zeros(mavs: list):
#     inPositive = False
#     points = []
#     # index one of the mav's data
#     for i in range(len(mavs[0])):
#         if mavs[0][i] > 0 and mavs[1][i] > 0 and mavs[2][i] > 0:
#             if not inPositive:
#                 inPositive = True
#                 points.append(i)
#         else:
#             if inPositive:
#                 inPositive = False
#                 # sell point perhaps
#     return points

first_dev_35 = stock.charts['1d'].mav_dy[35]
first_dev_14 = stock.charts['1d'].mav_dy[14]
first_dev_7 = stock.charts['1d'].mav_dy[7]

fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(data)
ax2.plot(first_dev_35)
ax3.plot(first_dev_14)

for point in stock.charts['1d'].buy_lines(7)[0]:
    ax1.axvline(x=point)

plt.show()