from stock import Stock
from algochart import AlgoChart


def garb(stock):
    hourly = stock.charts['1h']
    daily = stock.charts['1d']
    weekly = stock.charts['1wk']


    def get_buy_sell_amounts(chart, margin):
        buy_amount = 0
        sell_amount = 0

        if chart.buy_n_sell_lines[-1] == len(chart.dates) - 1:
            buy_amount += 1
            if chart.ma_scale()[-1] > 1 - margin:
                buy_amount += 1
            if chart.horizontal_scale()[-1] > 1 - margin:
                buy_amount += 1
            if buy_amount == 3:
                buy_amount += 1

        elif chart.buy_n_sell_lines[-1] == len(chart.dates) - 1:
            sell_amount += 1
            if chart.ma_scale()[-1] < margin:
                sell_amount += 1
            if chart.horizontal_scale()[-1] < margin:
                sell_amount += 1
            if sell_amount == 3:
                sell_amount += 1

        else:
            if chart.combined_scales()[-1] > 1 - margin:
                buy_amount += 2
            elif chart.combined_scales()[-1] < margin:
                sell_amount += 2

        return buy_amount, sell_amount

    buy, sell = get_buy_sell_amounts(hourly, 0.55)

def one()

