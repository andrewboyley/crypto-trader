import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import *
import numpy as np
import pickle
import talib
from binance.client import Client
from config import *
from Bot import Bot


print("--- CRYPTO TRADING BOT ---\n")
bot = Bot()
bot.run()


# plt.plot(df['Open Time'], df['Close'])
# # plt.plot(df['Open Time'],ema8)
# # plt.plot(df['Open Time'],ema13)
# # plt.plot(df['Open Time'],ema21)
# # plt.plot(df['Open Time'],ema34)
# # plt.plot(df['Open Time'],ema55)

# longs = df[df['Decision'] == 'Long']
# exits = df[df['Decision'] == 'Exit Long']


# plt.scatter(longs['Open Time'], longs['Close'], marker='^', c='#00ff00')
# plt.scatter(exits['Open Time'], exits['Close'],marker='v',c='#ff0000')

# plt.xticks(rotation = 20)
# plt.show()
