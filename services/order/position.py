from services.auth.auth import exchange_data


class Position:
    def __init__(self):
        self.symbol = None
        self.price = None
        self.amount = None
        self.status = OrderStatus.START

    def add_to_buy(self, symbol, amount, price):
        self.price = price
        self.amount = amount
        self.status = OrderStatus.BUY_APPROVED
        self.symbol = symbol

    def add_to_sell(self, symbol, amount, price):
        self.price = price
        self.amount = amount
        self.status = OrderStatus.SELL_APPROVED
        self.symbol = symbol

    def buy(self):
        if self.status == OrderStatus.BUY_APPROVED:
            try:
                exchange_data.create_limit_buy_order(self.symbol, self.amount, self.price * 1.005)
                self.status = OrderStatus.OPEN_BUY
            except:
                self.status = OrderStatus.BUY_FAILED

    def sell(self):
        if self.status == OrderStatus.SELL_APPROVED:
            try:
                exchange_data.create_limit_sell_order(self.symbol, self.amount, self.price * 0.995)
                self.status = OrderStatus.OPEN_SELL
            except:
                self.status = OrderStatus.SELL_FAILED

    def check_open_orders(self):
        if self.status not in [OrderStatus.OPEN_SELL, OrderStatus.OPEN_BUY]:
            return
        orders = exchange_data.fetch_open_orders(self.symbol)
        if len(orders) == 0:
            if self.status == OrderStatus.OPEN_SELL:
                self.status = OrderStatus.SOLD
            if self.status == OrderStatus.OPEN_BUY:
                self.status = OrderStatus.SOLD
        if len(orders) > 1:
            print("Too many Orders. Please fix manually.")


from enum import Enum


class OrderStatus(Enum):
    START = 0
    SELL_APPROVED = 1
    BUY_APPROVED = 2
    SELL_FAILED = 3
    BUY_FAILED = 4
    OPEN_SELL = 5
    OPEN_BUY = 6
    SOLD = 7
    BOUGHT = 8
