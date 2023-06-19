from stock import Stock
from trading_bot import Bot
import numpy.random as random
import schedule
import time
import matplotlib.pyplot as plt
from reddit_scraper import scrape_reddit
cm = plt.cm.get_cmap('RdYlGn')


current_trades = [] # list of stock objects
quantity = 100


class Algo:
    def __init__(self):
        """Params"""
        self.period = '20d'
        self.timeframe = '5m'
        self.quantity = 100

        self.tickers = ['tsla', 'amd', 'nvda', 'aapl', 'msft', 'cni', 'ko', 'amc', 'td', 'crsp', 'spce', 'sq', 'pypl']
        self.stocks = [Stock(ticker, self.period, self.timeframe) for ticker in self.tickers]
        self.setups = self.get_setups()
        self.open_trades = []

    def scrape_stocks(self):
        stocks = scrape_reddit()
        sorted_stocks = dict(sorted(stocks.items(), key=lambda item: item[1], reverse=True))
        stocks = {}
        for k, v in list(sorted_stocks.items()):
            stocks[k.upper().replace('$', '')] = v
        # maybe append if not already in
        return stocks

    def get_setups(self):
        setups = []
        for stock in self.stocks:
            try:
                colours = list(stock.charts[self.timeframe].combined_scales())
                if colours[-2] <= 0.55:
                    if colours[-1] >= 0.55:
                        setups.append(stock)
            except:
                pass
        return setups

    def manage_trades(self):
        """Find/trade any settups at current candle"""
        print('Managing Trades...')
        for stock in self.get_setups():
            if stock not in self.open_trades:
                print('Buying: ' + stock.ticker)
                order_id = stock.charts[self.timeframe].dates[-1].time().hour + random.random(9999)
                Bot(stock.ticker, 'BUY', self.quantity, order_id)
                self.open_trades.append(stock)

        """Sell any stocks that are in sell zone"""
        for stock in self.open_trades:
            colours = list(stock.charts[self.timeframe].combined_scales())
            if list(colours)[-1] <= 0.45:
                order_id = stock.charts[self.timeframe].dates[-1].time().hour + random.randint(9999)
                print('Selling: ' + stock.ticker)
                Bot(stock.ticker, 'SELL', self.quantity, order_id)
                self.open_trades.remove(stock)


"""Run Bot"""
algo = Algo()

schedule.every(5).minutes.unitl('1')
schedule.every(5).minutes.until('16:00').do(algo.manage_trades)

while True:
    schedule.run_pending()
    time.sleep(1)
    