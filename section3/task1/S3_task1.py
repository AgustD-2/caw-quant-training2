import websockets
from datetime import datetime 
from binance.websockets import BinanceSocketManager
from binance.client import Client
import os
import keys
#import json
import pandas as pd

def process_msg(msg):
    file_exists = os.path.isfile('S3_task1.csv')
    old_dict=msg["k"]
    wanted_keys=('c','h', 'l', 'o', 'v')
    new_dict={k: old_dict[k] for k in set(wanted_keys)&set(old_dict.keys())}
    new_dict['datetime']=datetime.fromtimestamp(msg['E'] // 1000)
    new_data=pd.DataFrame.from_dict([new_dict])
    new_data=new_data.rename({'c':'close', 'h': 'high', 'l': 'low', 'o':'open', 'v':'volume'}, axis=1)
    if not file_exists:
        new_data.to_csv('S3_task1.csv', mode='a', header=True, index=False)
    else:
        new_data.to_csv('S3_task1.csv', mode='a', header=False, index=False)

client=Client(api_key=keys.Pkeys, api_secret=keys.Skeys)
bm=BinanceSocketManager(client)
conn_key=bm.start_kline_socket('ETHBTC', process_msg, client.KLINE_INTERVAL_1MINUTE)
bm.start()
bm.close()
