import os

import ccxt as ccxt
from binance.client import Client

# init
api_key = 'ZHyp4Nfdygb9Gchz87POO9WGgEYm5Hh4VG7XmEBbqjF5VKbAVcQb4VWvThAT4HSi'
api_secret = 'y5PVAA3CpETEVuHaTTDnBthAdrmOWRdqdMguFwkvvETkpijI8JVIdRHDK7sO5tv2'


# api_key = os.environ['binance_api']
# api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)

exchange_data = ccxt.binance({'apiKey':api_key,
                         'secret': api_secret})

market_data = exchange_data.load_markets()

