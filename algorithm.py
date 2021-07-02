from stock import Stock
from algochart import AlgoChart


tesla = Stock('TSLA')
stock_list = [tesla]


def zero():
    for stock in stock_list:

        hourly = stock.charts['1h']
        daily = stock.charts['1d']
        weekly = stock.charts['1wk']

        for hour in range(168, len(hourly)):
            hourly_data = hourly.ticker, hourly.period, hourly.timeframe, hourly.dates[:hour], hourly.opens[:hour], hourly.closes[:hour], hourly.highs[:hour], hourly.lows[:hour]
            one(AlgoChart(hourly_data), hour)






            for day in range(7, len(daily)):
                daily_data = daily.ticker, daily.period, daily.timeframe, daily.dates[:hour], daily.opens[:hour], daily.closes[:hour], daily.highs[:hour], daily.lows[:hour]
                one(AlgoChart(daily_data), day)

                for week in range(1, len(weekly)):
                    weekly_data = weekly.ticker, weekly.period, weekly.timeframe, weekly.dates[:hour], weekly.opens[:hour], weekly.closes[:hour], weekly.highs[:hour], weekly.lows[:hour]
                    one(AlgoChart(weekly_data), week)


def one(chart, limit):
    chart.evaluate()
