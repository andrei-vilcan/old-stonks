class Candle:
    """
    a candle

    stores:
    date
    open
    close
    difference
    colour
    """
    date: str
    open: float
    close: float
    difference: float
    high: float
    low: float

    def __init__(self, date: str, open: float, close: float, high: float, low: float):
        self.date = date
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.difference = self.close - self.open

    def date(self):
        return self.date

    def open(self):
        return self.open

    def close(self):
        return self.close

    def difference(self):
        return self.difference

    def high(self):
        return self.high

    def low(self):
        return self.low
    