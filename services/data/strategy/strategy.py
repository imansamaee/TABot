class Strategy:
    def __init__(self, data):
        self.data = data
        self.ta = data.df.ta
        # self.ohlc = resample(data.df, data.timeframe)

    def rsi_macd_stoch_buy(self, stoch_max=50, rsi_min=60):
        stoch = self.ta.stoch().iloc[-1]['STOCHk_14_3_3'] < stoch_max and self.ta.stoch().iloc[-1][
            'STOCHd_14_3_3'] < stoch_max
        rsi_min = self.ta.rsi().iloc[-1] > rsi_min
        macd = self.ta.macd()['MACD_12_26_9'].iloc[-1] > self.ta.macd()['MACDs_12_26_9'].iloc[-1] < 0
        if rsi_min:
            print(self.data.symbol, stoch, rsi_min, macd)
        return stoch and rsi_min and macd

    def scalping_buy(self):
        '''
        https://youtu.be/MK47z07tGNM
        :return: bool
        '''
        from bot.bot import TRADING_BOT
        df = self.data.df
        symbol_data = TRADING_BOT.state.symbols[self.data.symbol]
        if "scalping" not in symbol_data:
            symbol_data["scalping"] = []
        self.data.indicators.smma(period=21, column_name='smma_21', apply_to='close')
        self.data.indicators.smma(period=50, column_name='smma_50', apply_to='close')
        self.data.indicators.smma(period=200, column_name='smma_200', apply_to='close')
        self.data.indicators.fractals(column_name_high='fractals_high', column_name_low='fractals_low')
        self.data.df = self.data.indicators.df
        rsi = self.ta.rsi().iloc[-1]
        fractals_low = df['fractals_low'].iloc[-3]
        fractals_high = df['fractals_high'].iloc[-3]
        smma_21 = df['smma_21'].iloc[-1]
        smma_50 = df['smma_50'].iloc[-1]
        smma_200 = df['smma_200'].iloc[-1]
        symbol_data["scalping"].append({'rsi': rsi,
                                        'fractals_low': fractals_low,
                                        'fractals_high': fractals_high,
                                        'smma_21': smma_21,
                                        'smma_50':smma_50,
                                        'smma_200': smma_200})

        if symbol_data["scalping"][-1]['fractals_low']:
            print(self.data.symbol)

    def breakout(self, percentage=2):
        recent_c = self.data.df[-16:-1]
        threshold = 1 - percentage / 100
        max_close = recent_c['close'].max()
        min_close = recent_c['close'].min()
        consolidating = min_close > max_close * threshold
        is_broken_out = max_close < self.data.df[-1:]['close'].values[0]
        return consolidating and is_broken_out
