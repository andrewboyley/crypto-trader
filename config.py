from dotenv import load_dotenv
load_dotenv()

import os

API = os.getenv("API")
SECRET = os.getenv("SECRET")

base_url = 'https://api.binance.com'

market = 'BTCUSDT'
tick_interval = '1h'

