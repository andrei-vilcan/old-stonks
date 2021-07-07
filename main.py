from stock import Stock
from trading_bot import Bot
import schedule, time
import matplotlib.pyplot as plt
cm = plt.cm.get_cmap('RdYlGn')
from reddit_scraper import scrape_reddit
# from twitter_scraper import scrape_twitter

"""Params"""
period = '30d'
timeframe = '30m'
current_orders = {}

tickers = ['tsla', 'amd', 'nvda', 'aapl', 'msft', 'cni', 'ko', 'amc', 'td', 'crsp', 'spce', '']
stocks = [Stock(ticker, period, timeframe) for ticker in tickers]

def scrape_stocks(p=period, t=timeframe):
    stocks = scrape_reddit()
    for k,v in stocks.items():
        


def get_setups(stocks, t=timeframe):
    setups = []
    for stock in stocks:
        try:
            colours = list(stock.charts[t].combined_scales())
            if colours[-2] <= 0.55:
                if colours[-1] >= 0.55:
                    setups.append(stock)
                    print(stock)
        except:
            pass
    return setups


def graph_chart(stock, t=timeframe):
    prices = list(stock.charts[t].closes)
    colours = list(stock.charts[t].combined_scales())
    plt.scatter(x=range(len(prices)), y=prices, c=colours, cmap=cm)
    plt.show()


schedule.every().day.at('8:30').do(scrape_stocks)



# while True:
#     schedule.run_pending()
#     time.sleep(1)