import os
from binance.client import Client

from dotenv import load_dotenv
load_dotenv()


API = os.getenv("API")
SECRET = os.getenv("SECRET")

markets = ['BTC','ETH','BNB','DOGE','ADA','UNI','LTC']
tick_interval = Client.KLINE_INTERVAL_30MINUTE
