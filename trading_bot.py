import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import numpy.random as random
import threading
import time


class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)


class Bot():
    ib = None

    def __init__(self, ticker, action: str, quantity: int, orderId):
        self.ticker = ticker
        self.action = action
        self.quantity = quantity
        self.orderId = orderId

        self.ib = IBApi()
        self.ib.connect('127.0.0.1', 7497, 1)
        ib_thread = threading.Thread(target=self.runLoop, daemon=True)
        ib_thread.start()
        time.sleep(1)

        self.ib.placeOrder(self.orderId, self.make_contract(), self.make_order())
        time.sleep(1)
        self.ib.disconnect()

    def make_contract(self):
        contract = Contract()
        contract.symbol = self.ticker.upper()
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.primaryExchange = 'ISLAND'
        contract.currency = 'USD'
        time.sleep(1)
        return contract

    def make_order(self):
        order = Order()
        order.orderType = 'MKT'
        order.action = self.action
        order.totalQuantity = self.quantity
        return order


    def runLoop(self):
        self.ib.run()