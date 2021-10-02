import pandas as pd
import pandas_ta as ta
from tapy import Indicators
from services.auth.auth import exchange_data
from services.data.indicators.indicators import Indicator
from services.data.strategy.strategy import Strategy
from services.plotting.candlestick import draw_chart


class DataObject:
    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        self.df = get_df(self.symbol, self.timeframe)
        self.ind = Indicator(self)
        self.strategy = Strategy(self)
        self.ticker = exchange_data.fetch_ticker(symbol)
        self.quote_volume_24h = self.ticker['quoteVolume']
        self.indicators = Indicators(self.df, open_col='open', high_col='high', low_col='low', close_col='close', volume_col='volume')

    def draw_chart(self):
        draw_chart(self)


def get_df(symbol, timeframe):
    bars = exchange_data.fetch_ohlcv(symbol, timeframe=timeframe, limit=200)
    df = pd.DataFrame(bars, columns=["time", "open", "high", "low", "close", "volume"])
    df.title = symbol
    df.timeframe = timeframe
    return df
