import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time
orderId = 1

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    def nextValidId(self, nextOrderId:int):
        global orderId
        orderId = nextOrderId


class Bot():
    ib = None

    def __init__(self, symbol, action: str, quantity: int, order_id: int):
        self. ib = IBApi()
        self.ib.connect('127.0.0.1', 7497, 1)
        ib_thread = threading.Thread(target=self.runLoop, daemon=True)
        ib_thread.start()
        time.sleep(1)

        self.symbol = symbol
        self.contract.symbol = symbol.upper()
        self.contract = Contract()
        self.contract.secType = 'STK'
        self.contract.exchange = 'SMART'
        self.contract.primaryExchange = 'ISLAND'
        self.contract.currency = 'USD'

        # check for open orders before making one
        order = Order()
        order.orderType = 'MKT'
        order.action = action
        order.totalQuantity = quantity
        self.ib.placeOrder(order_id, self.contract, order)

    def runLoop(self):
        self.ib.run()