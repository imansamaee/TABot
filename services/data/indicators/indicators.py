class Indicator:
    def __init__(self, data):
        self.data = data

    def macd_buy_signal(self):
        return self.data.df.iloc[-1]['macd'] < 0 and\
               1 < len(self.data.df) - self.data.df['macd'].idxmin() < 4
