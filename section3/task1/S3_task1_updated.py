import websockets
from datetime import datetime
from binance.websockets import BinanceSocketManager
from binance.client import Client
import os
import keys
#import json
import pandas as pd

wanted_keys = ('c', 'h', 'l', 'o', 'v')


def process_msg(msg):
    if msg['k']['x'] == True:
        file_exists = os.path.exists('S3_task1.csv')
        old_dict = msg["k"]
        new_dict = {k: old_dict[k]
                    for k in old_dict.keys() if k in wanted_keys}
        new_data = pd.DataFrame(
            new_dict, index=[datetime.fromtimestamp(msg['E'] // 1000)])
        new_data = new_data.rename(
            {'c': 'close', 'h': 'high', 'l': 'low', 'o': 'open', 'v': 'volume'}, axis=1)
        new_data.to_csv('S3_task1.csv', mode='a',
                        header=not file_exists, index=True)


client = Client(api_key=keys.Pkeys, api_secret=keys.Skeys)
bm = BinanceSocketManager(client)
conn_key = bm.start_kline_socket(
    'ETHBTC', process_msg, client.KLINE_INTERVAL_1MINUTE)
bm.start()
