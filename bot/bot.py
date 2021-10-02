import time

import schedule

from services import API_DATA
from services.data.dataObject.data_object import DataObject
from services.order.position import OrderStatus
from services.scheduleJob.schedule_job import scheduled
from services.state.state import State


class BOT:
    def __init__(self, time_frame="15m", limit=200, base_amount=40):
        self.time_frame = time_frame
        self.limit = limit
        self.state = State()
        self.base_amount = base_amount


TRADING_BOT = BOT(time_frame="1m", limit=200, base_amount=40)


@scheduled(TRADING_BOT.time_frame)
def get_macd_buy_signal(min_quote_volume_24h_M=2.0):
    if TRADING_BOT.state.position.status is OrderStatus.BOUGHT:
        return
    approved_count = 0
    print('searching trades...')
    for symbol in API_DATA.trade_symbols:
        if symbol not in TRADING_BOT.state.symbols:
            TRADING_BOT.state.symbols[symbol] = {}
        data = DataObject(symbol, TRADING_BOT.time_frame)
        # data.draw_chart()
        # break
        a = data.strategy.scalping_buy()
        if data.quote_volume_24h > min_quote_volume_24h_M * 1000000:
            pass
            # if data.strategy.breakout() and data.strategy.rsi_macd_stoch_buy():
            #     data.draw_chart()
            #     TRADING_BOT.state.position.add_to_buy(symbol)
            #     approved_count += 1
    print(f'Done! {approved_count} trades found. Next search in {TRADING_BOT.time_frame}...')


@scheduled("1s")
def update_status():
    TRADING_BOT.state.update()
    pass


def run():
    get_macd_buy_signal()
    update_status()
    while True:
        schedule.run_pending()
        time.sleep(1)
