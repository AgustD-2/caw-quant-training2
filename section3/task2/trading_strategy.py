from binance.client import Client
import pandas as pd
import data_fetcher as df
import keys
from binance.websockets import BinanceSocketManager


class strategy():

    def __init__(self, in_the_market, asset, frequency, bm):
        self.in_the_market = in_the_market
        
        # should be a dataframe containing the two indicators(fast and slow)
        self.data = df.data_fetcher()
        
        self.fast = self.data[0]
        self.slow = self.data[1]

    def create_market_buy(self, asset, client):
        in_the_market = True
        order = client.create_test_order(
            symbol=asset, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=100)
        print('Buy')

    def create_market_sell(self, asset, client):
        in_the_market = False
        order = client.create_test_order(
            symbol=asset, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=100)
        print('Sell')

    def cross_up(self):
        if self.fast[0] > self.slow[0] and self.slow[-1] > self.fast[-1]:
            return True
        else:
            return False

    def cross_down(self):
        if self.fast[0] < self.slow[0] and self.slow[-1] < self.fast[-1]:
            return True
        else:
            return False
