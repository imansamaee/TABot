from services.order.position import Position


class State:
    def __init__(self):
        self.position = Position()
        self.symbols = {}

    def update(self):
        self.position.buy()
        self.position.sell()
        self.position.check_open_orders()