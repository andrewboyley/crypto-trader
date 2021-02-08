import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import *
import numpy as np
import pickle
import time
import hmac
import hashlib
from urllib.parse import urljoin, urlencode


def binanceDataFrame(klines):
    df = pd.DataFrame(klines.reshape(-1, 12), dtype=float, columns=('Open Time',
                                                                    'Open',
                                                                    'High',
                                                                    'Low',
                                                                    'Close',
                                                                    'Volume',
                                                                    'Close time',
                                                                    'Quote asset volume',
                                                                    'Number of trades',
                                                                    'Taker buy base asset volume',
                                                                    'Taker buy quote asset volume',
                                                                    'Ignore'))
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    return df


def saveDataFrame(df, file_name):
    outfile = open(file_name, 'wb')
    pickle.dump(df, outfile)

    outfile.close()

def openDataframe(file_name):
    outfile = open(file_name, 'rb')
    df = pickle.load(outfile)

    outfile.close()

    return df

path = '/sapi/v1/accountSnapshot'

headers = {
    'X-MBX-APIKEY': API
}

timestamp = int(time.time() * 1000)

params = {
    'type': "SPOT",
    'timestamp': timestamp
}

query_string = urlencode(params)
params['signature'] = hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

query_string = urlencode(params)

url = urljoin(base_url, path)

wallet = requests.get(url,headers=headers,params=params).json()


print(wallet)

# candles = requests.get(
#     f'{url}/api/v3/klines?symbol={market}&interval={tick_interval}').json()

# df = binanceDataFrame(np.array(candles))

# saveDataFrame(df, 'Klines')
# df = openDataframe('Klines')

# df.plot(x='Open Time', y='Close', kind='line')
# plt.show()

