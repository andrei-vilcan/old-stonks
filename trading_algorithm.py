from stock import Stock
import schedule
import time
from trading_bot import Bot
from random import *

tsla = Stock('TSLA', None, '5m')
nvda = Stock('NVDA', None, '5m')
cni = Stock('CNI', None, '5m')
amd = Stock('AMD', None, '5m')
aapl = Stock('AAPL', None, '5m')
ko = Stock('KO', None, '5m')
amc = Stock('AMC', None, '5m')
td = Stock('TD', None, '5m')
crsp = Stock('CRSP', None, '5m')
spce = Stock('SPCE', None, '5m')
stock_list = [tsla, nvda, cni, amd, aapl, ko, amc, td, crsp, spce]


def order_id():
    return random.randint(1, 100000)


def zero(stocks):
    for stock in stocks:
        weekly_action = 0
        daily_action = 0
        hourly_action = 0
        # updates = stock.update()
        # if updates[2]:
        #     weekly_action = one(stock.charts['1wk'])
        # if updates[1]:
        #     daily_action = one(stock.charts['1d'])
        # if updates[0]:
        #     hourly_action = one(stock.charts['1h'])

        five_min_action = one(stock.charts['5m'])

        if weekly_action > 0:
            daily_action += weekly_action
        if daily_action > 0:
            hourly_action += daily_action

        if five_min_action > 0:
            action = 'BUY'
        elif five_min_action < 0:
            action = 'SELL'
        else:
            continue

        Bot(stock.ticker, action, 100, order_id())


def one(chart):
    buy_groups = chart.buy_n_sell_lines(9, 0.33, True)[0]
    sell_groups = chart.buy_n_sell_lines(9, 0.33, True)[1]

    buy_prices = []
    for i in range(len(buy_groups[-1]) - 1):
        buy_prices.append(chart.closes[buy_groups[-1][i]])
    sell_prices = []
    for i in range(len(sell_groups[-1]) - 1):
        sell_prices.append(chart.closes[sell_groups[-1][i]])

    if buy_groups[-1][-1] - 1 == len(chart.closes):
        if 1 < len(buy_groups[-1]) < 4:
            if chart.closes[buy_groups[-1][-1]] < min(buy_prices):
                action = 1
            else:
                action = 0
        else:
            action = 1
    elif sell_groups[-1][-1] - 1 == len(chart.closes):
        if 1 < len(sell_groups[-1]) < 4:
            if chart.closes[sell_groups[-1][-1]] < max(sell_prices):
                action = -1
            else:
                action = 0
        else:
            action = -1
    else:
        action = 0
    return action


schedule.every(5).minutes.do(zero(stock_list))

while True:
    schedule.run_pending()
    time.sleep(1)

