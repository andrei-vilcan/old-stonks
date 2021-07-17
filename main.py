from stock import Stock
from trading_bot import Bot
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
        # self.period = '2d'
        # self.timeframe = '2m'
        self.quantity = 100
        self.orderId = 1
        #self.tickers = ['tsla', 'amd', 'nvda', 'aapl', 'msft', 'cni', 'ko', 'amc', 'crsp', 'spce', 'sq', 'pypl']
        self.tickers = ['tsla', 'amd', 'amc', 'crsp', 'spce', 'sq', 'pypl']
        self.stocks = []
        self.open_trades = []
        self.setups = []

    def scrape_stocks(self):
        stocks = scrape_reddit()
        sorted_stocks = dict(sorted(stocks.items(), key=lambda item: item[1], reverse=True))
        stocks = {}
        for k, v in list(sorted_stocks.items()):
            stocks[k.upper().replace('$', '')] = v
        # maybe append if not already in
        return stocks

    def create_stock_objs(self):
        stocks = []
        for ticker in self.tickers:
            try:
                stocks.append(Stock(ticker))
                time.sleep(3)
                print('Grabbing info for ' + ticker)
            except:
                pass

        self.stocks = stocks

    def get_setups(self):
        setups = []
        print('Finding setups...')
        self.create_stock_objs()
        for stock in self.stocks:
            try:
                colours = list(stock.chart.combined_scales())
                if colours[-2] <= 0.375 or colours[-3] <= 0.375:
                    if colours[-1] >= 0.425:
                        setups.append(stock)
                        print('Setup found!: ' + stock.ticker.upper())
            except:
                pass
        if len(setups) == 0:
            print('No setups found.')
        return setups

    def manage_trades(self):
        """Find/trade any settups at current candle"""
        text = 'Open Trades: '
        if not self.open_trades:
            text = text + 'None.'
        if self.open_trades:
            for ticker in self.open_trades:
                text = text + ticker + ' '
        print(text)

        print('Managing Trades...')
        for stock in self.get_setups():
            if stock.ticker not in self.open_trades:
                Bot(stock.ticker, 'BUY', self.quantity, self.orderId)
                self.update_orderId()
                self.open_trades.append(stock.ticker)
                print('\033[1;32;40m' + 'Buying: ' + stock.ticker)
                time.sleep(1)

        """Sell any stocks that are in sell zone"""
        for ticker in self.open_trades:
            stock = Stock(ticker)
            colours = stock.chart.combined_scales()
            if list(colours)[-1] <= 0.375:
                Bot(stock.ticker, 'SELL', self.quantity, self.orderId)
                self.update_orderId()
                self.open_trades.remove(stock.ticker)
                print('\033[1;33;40m' + 'Selling: ' + stock.ticker)
                time.sleep(1)

    def update_orderId(self):
        self.orderId += 1


"""Run Bot"""
algo = Algo()

schedule.every().hour.at(':00').do(algo.manage_trades)
schedule.every().hour.at(':05').do(algo.manage_trades)
schedule.every().hour.at(':10').do(algo.manage_trades)
schedule.every().hour.at(':15').do(algo.manage_trades)
schedule.every().hour.at(':20').do(algo.manage_trades)
schedule.every().hour.at(':25').do(algo.manage_trades)
schedule.every().hour.at(':30').do(algo.manage_trades)
schedule.every().hour.at(':35').do(algo.manage_trades)
schedule.every().hour.at(':40').do(algo.manage_trades)
schedule.every().hour.at(':45').do(algo.manage_trades)
schedule.every().hour.at(':50').do(algo.manage_trades)
schedule.every().hour.at(':55').do(algo.manage_trades)


while True:
    schedule.run_pending()
    time.sleep(1)