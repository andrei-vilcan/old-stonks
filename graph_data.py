from stock import Stock
import mplfinance as mpf

stonk = Stock('TD')
lines = stonk.charts['1wk'].getLevels()
for candle in stonk.charts['1mo'].candles:
    try:
        lines.append(candle.close)
    except Exception as e:
        print(str(e))
        pass

mpf.plot(stonk.charts['1d'].data, mav=(50), hlines=lines, type='candle', style='charles')