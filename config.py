import os
from binance.client import Client

from dotenv import load_dotenv
load_dotenv()


API = os.getenv("API")
SECRET = os.getenv("SECRET")

markets = ['BTC', 'ETH', 'DOGE', 'BNB']
tick_interval = Client.KLINE_INTERVAL_30MINUTE
