import websockets
import talib
import pandas as pd
import numpy as np
import keys
from binance.websockets import BinanceSocketManager
from binance.client import Client

wanted_keys = ('c', 'h', 'l', 'o', 'v')
close_old = pd.DataFrame([])
indicator_df1 = pd.DataFrame([])
period1 = 2
period2 = 3

'''
This data_fetcher function was written as a callback function for the start_kline_socket method 
and have to be used as bm.start_kline_socket('ETHBTC', data_fetcher, client.KLINE_INTERVAL_1MINUTE). 
But I meant to use it directly and get the indicator data for use in the strategy module. 
'''


def data_fetcher(msg):
    global close_old
    if msg['k']['x'] == True:
        old_dict = msg["k"]
        new_dict = {k: old_dict[k]
                    for k in old_dict.keys() if k in wanted_keys}
        new_data = pd.DataFrame(new_dict, index=[0])
        new_data = new_data['c']
        close_old = close_old.append(new_data)
        close_new = close_old[0]
        close = close_new.to_numpy(dtype='float')
        pfast = talib.SMA(close, timeperiod=period1)
        pslow = talib.SMA(close, timeperiod=period2)
        d = {'fast': pfast, 'slow': pslow}
        indicator_df = pd.DataFrame(data=d)
        # print(indicator_df)
        return indicator_df
