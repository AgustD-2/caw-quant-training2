import talib
import pandas as pd
from binance.websockets import BinanceSocketManager
from binance.client import Client
import data_fetcher as df
import trading_strategy as ts
import keys


client = Client(api_key=keys.Pkeys, api_secret=keys.Skeys)
bm = BinanceSocketManager(client)
asset = 'ETHBTC'
frequency = client.KLINE_INTERVAL_1MINUTE


strat = ts.strategy(False, asset, frequency, bm)
# print(strat.data)
if strat.cross_up() and not strat.in_the_market:
    strat.create_market_buy(asset, client)
elif strat.cross_down() and strat.in_the_market:
    strat.create_market_sell(asset, client)
