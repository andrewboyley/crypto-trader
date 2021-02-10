import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import *
import numpy as np
import pickle
import talib
import numpy
from binance.client import Client
from config import *


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


# client = Client(API,SECRET)

# klines = client.get_klines(symbol="BTCUSDT",interval=Client.KLINE_INTERVAL_30MINUTE)

# saveDataFrame(klines,'Klines.pickle')

klines = openDataframe('Klines.pickle')

df = binanceDataFrame(numpy.array(klines))


def populate_buys(df):
    df['Decision'] = 'Nothing'

    # ----------
    #  MOMENTUM 
    # ----------

    ema8 = talib.EMA(df['Close'],timeperiod=8)
    ema13 = talib.EMA(df['Close'],timeperiod=13)
    ema21 = talib.EMA(df['Close'],timeperiod=21)
    ema34 = talib.EMA(df['Close'],timeperiod=34)
    ema55 = talib.EMA(df['Close'],timeperiod=55)

    # ----------
    #  OSCILLATORS 
    # ----------

    rsi = talib.RSI(df['Close'], timeperiod=14)

    # ----------
    #  STOCHASTIC 
    # ----------

    kFast,dFast = talib.STOCHF(df['High'], df['Low'],df['Close'],  fastk_period=14)

    # ----------
    #  STRATEGY 
    # ----------

    #  0 - No position
    # -1 - Entered Long
    #  1 - Entered Short
    position = 0

    for i in range(len(df)):
        # MOMENTUM
        ema8i,ema13i,ema21i,ema34i,ema55i = ema8[i],ema13[i],ema21[i],ema34[i],ema55[i]

        if not(ema8i and ema13i and ema21i and ema34i and ema55i):
            continue

        longEmaCondition = ema8i > ema13i and ema13i > ema21i and ema21i > ema34i and ema34i > ema55i
        exitLongEmaCondition = ema13i < ema55i

        # RSI
        rsii = rsi[i]

        if not(rsii):
            continue

        longRsiCondition = rsii < 70 and rsii > 40
        exitLongRsiCondition = rsii > 70

        #STOCHASTIC

        kFasti = kFast[i]

        if not kFasti:
            continue

        longStochasticCondition = kFasti < 80
        exitLongStochasticCondition = kFasti > 95

        #STRAT

        longCondition = longEmaCondition and longRsiCondition and longStochasticCondition and position == 0
        exitLongCondition = (exitLongEmaCondition or exitLongRsiCondition or exitLongStochasticCondition) and position == -1

        if longCondition:
            df['Decision'][i] = 'Long'
            position = -1
        elif exitLongCondition:
            df['Decision'][i] = 'Exit Long'
            position = 0
        else:
            df['Decision'][i] = 'Hold'

        #TODO: Do shorts
    print()



populate_buys(df)


plt.plot(df['Open Time'], df['Close'])
# plt.plot(df['Open Time'],ema8)
# plt.plot(df['Open Time'],ema13)
# plt.plot(df['Open Time'],ema21)
# plt.plot(df['Open Time'],ema34)
# plt.plot(df['Open Time'],ema55)

longs = df[df['Decision'] == 'Long']
exits = df[df['Decision'] == 'Exit Long']


plt.scatter(longs['Open Time'], longs['Close'], marker='^', c='#00ff00')
plt.scatter(exits['Open Time'], exits['Close'],marker='v',c='#ff0000')

plt.xticks(rotation = 20)
plt.show()

