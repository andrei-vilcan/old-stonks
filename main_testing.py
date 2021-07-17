from stock import Stock
import schedule
import time
import matplotlib.pyplot as plt
from reddit_scraper import scrape_reddit
cm = plt.cm.get_cmap('RdYlGn')


current_trades = [] # list of stock objects
quantity = 100
# completed_trades = {'tsla': [], 'amd': [], 'nvda': [], 'aapl': [], 'msft': [], 'cni': [], 'ko': [], 'amc': [], 'crsp': [], 'spce': [], 'sq': [], 'pypl': [], 'pins': []}
completed_trades = {'xrp-usd': [], 'btc-usd': [], 'eth-usd': [], 'ada-usd': [], 'xlm-usd': [], 'bnb-usd': [], 'eos-usd': [], 'bch-usd': [], 'hex-usd': [], 'doge-usd': [], 'ltc-usd': []}


class Algo:
    def __init__(self):
        """Params"""
        # self.period = '2d'
        # self.timeframe = '2m'
        self.quantity = 100
        self.orderId = 1
        # self.tickers = ['tsla', 'amd', 'nvda', 'aapl', 'msft', 'cni', 'ko', 'amc', 'crsp', 'spce', 'sq', 'pypl', 'pins']
        self.tickers = ['xrp-usd', 'btc-usd', 'eth-usd', 'ada-usd', 'xlm-usd', 'bnb-usd', 'eos-usd', 'bch-usd', 'hex-usd', 'doge-usd', 'ltc-usd']
        self.stocks = []
        self.open_trades = []
        self.setups = []
        self.trades = {}

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
                print('\033[1;33;40m' + 'Grabbing info for ' + ticker)
                stocks.append(Stock(ticker, '30m'))
                time.sleep(1)
            except:
                pass

        self.stocks = stocks

    def get_setups(self):
        setups = []
        print('\033[1;33;40m' + 'Finding setups...')
        self.create_stock_objs()
        for stock in self.stocks:
            try:
                colours = list(stock.charts['30m'].combined_scales())
                if colours[-1] >= 0.775:
                    # use second last candle as this is called right after the candle is printed
                    setups.append(stock)
                    print('\033[1;32;40m' + 'Setup found!: ' + stock.ticker)
            except:
                pass
        if len(setups) == 0:
            print('\033[1;31;40m' + 'No setups found.')
        return setups

    def manage_trades(self):
        """Find/trade any settups at current candle"""
        text = 'Open Trades: '
        if not self.open_trades:
            text = text + 'None.'
        if self.open_trades:
            for ticker in self.open_trades:
                text = text + ticker + ' '
        print('\033[1;36;40m' + text)

        print('\033[1;35;40m' + 'Managing Trades...')
        buys = []
        for stock in self.get_setups():
            if stock.ticker not in self.open_trades:
                self.update_orderId()
                self.open_trades.append(stock.ticker)
                buys.append(stock.ticker)
                self.trades[stock.ticker] = stock.price()
                print('\033[1;32;40m' + 'Buying: ' + stock.ticker)
                time.sleep(1)

        """Sell any stocks that are in sell zone"""
        for ticker in self.open_trades:
            if ticker not in buys:
                stock = Stock(ticker)
                colours = list(stock.charts['30m'].combined_scales())
                if colours[-1] <= 0.275:
                    self.update_orderId()
                    self.open_trades.remove(stock.ticker)
                    percent_move = (stock.price() - self.trades[stock.ticker]) / self.trades[stock.ticker]
                    completed_trades[stock.ticker].append(percent_move)
                    print('\033[1;31;40m' + 'Selling: ' + stock.ticker)
                    time.sleep(1)

        print('\033[1;37;40m' + 'Completed Trades:')
        print(completed_trades)

    def update_orderId(self):
        self.orderId += 1


"""Run Bot"""
algo = Algo()

schedule.every().hour.at(':00').do(algo.manage_trades)
schedule.every().hour.at(':30').do(algo.manage_trades)


while True:
    schedule.run_pending()
    time.sleep(1)