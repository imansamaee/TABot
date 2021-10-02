from services.auth.auth import client


class APIData:
    def __init__(self, base_symbol):
        self.base_symbol = base_symbol
        self.ignore_list = ['USDCBUSD','AUDBUSD','USDPBUSD','TUSDBUSD']
        self.exchange_info = client.get_exchange_info()
        self.symbol_list_info = self.exchange_info['symbols']
        self.trade_symbols = self.init_trade_symbols()

    def init_trade_symbols(self):
        ts = [ts['symbol'] for ts in self.trading_spot_symbols_info if ts['symbol'].endswith(self.base_symbol) and ts['symbol'] not in self.ignore_list]
        return ts

    @property
    def trading_spot_symbols_info(self):
        return [s for s in self.symbol_list_info if s['status'] == "TRADING" and "SPOT" in s['permissions']]
