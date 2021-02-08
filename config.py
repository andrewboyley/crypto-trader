from dotenv import load_dotenv
load_dotenv()

import os

API = os.getenv("API")
SECRET = os.getenv("SECRET")

base_url = 'https://api.binance.com'

market = 'BTCUSDT'
tick_interval = '1h'

api = 'BqnnzhLffZk7QxP0Mbl7MkZVJJEUsD3TXyzUbiHSyjF6YucGUQprEPOvcLT4ul1Z'
secret = 'T9MsszRLRAmJtHroB8I9BAoEn0DAKrNtL7AfU0iLNkY5xhISQjad2YQZ84XfH1qH'