from config import API, SECRET, markets, tick_interval
from binance.client import Client
import pandas as pd
import numpy as np
from Util import *
from time import sleep
from Strategy import calculateIndicators, strategyDecision
import math


class Bot:
    def __init__(self):
        self.client = Client(API, SECRET)
        print("- Loaded API keys")

        self.usdt = 0
        self.position_val = 0
        self.balance = []
        self.bought = {}
        self.ticks = {}
        self.available_currencies = []
        self.refreshBalance()
        print('- Done fetching balance')
        self.generateBoughtStatus()
        self.generateTicks()

    def run(self):
        print("- Bot is running")
        print('\n--------TRADES-------\n')
        while True:
            for symbol in markets:
                symbol = symbol + 'USDT'
                klines = self.getKlines(symbol)

                # self.buy(symbol, klines)
                # sleep(5)
                # klines = self.getKlines(symbol)
                # self.sell(symbol, klines)
                # return

                ema8, ema13, ema21, ema34, ema55, rsi, kFast = calculateIndicators(
                    klines)

                enterLong, exitLong = strategyDecision(
                    ema8, ema13, ema21, ema34, ema55, rsi, kFast)

            if self.bought[symbol] is not None:
                if exitLong:
                    self.sell(symbol, klines)
            else:
                if enterLong:
                    self.buy(symbol, klines)

            # print('Waiting 5 seconds before next decision')
            sleep(10)

    def generateBoughtStatus(self):
        print('- Generating bought/sold statuses...')
        for coin in markets:
            coin += 'USDT'
            symbol_orders = self.client.get_all_orders(symbol=coin, limit=1)

            if len(symbol_orders) > 0 and symbol_orders[0]['side'] == 'BUY' and symbol_orders[0]['status'] == 'FILLED':
                self.bought[coin] = symbol_orders[0]
            else:
                self.bought[coin] = None

    def buy(self, symbol, df):
        self.refreshBalance()

        if self.usdt > 10:
            price = df["Close"][len(df) - 1]
            amount = self.usdt/price

            amount = truncate(amount, self.ticks[symbol])

            print(f'Buying {amount} {symbol} @ {price} USDT...')

            #buy_market = self.client.order_market_buy(symbol=symbol, quoteOrderQty=self.usdt)

            # self.bought[symbol] = buy_market

            # TESTING
            buy_market = self.client.create_test_order(
                symbol=symbol, side='BUY', type='MARKET', quoteOrderQty=self.usdt)

            self.bought[symbol] = {
                'type': 'BUY',
                'cummulativeQuoteQty': self.usdt,
                'executedQty': amount
            }
            ###

        else:
            print("Not enough USDT to trade (minimum of $10)")

    def sell(self, symbol, df):
        self.refreshBalance()

        # symbol_balance = 0
        # for s in self.balance:
        #     if s['asset'] + 'USDT' == symbol:
        #         symbol_balance = s['free']

        # TESTING
        symbol_balance = self.bought[symbol]['executedQty']
        ###

        price = df["Close"][len(df) - 1]

        if symbol_balance * price > 10:

            amount = truncate(symbol_balance, self.ticks[symbol])

            print(f'Selling {amount} {symbol} @ {price} USDT...')
            # self.client.order_market_sell(symbol=symbol, quantity=amount)

            # TESTING
            sell_market = self.client.create_test_order(
                symbol=symbol, side='SELL', type='MARKET', quantity=amount)

            sell_market = {
                'cummulativeQuoteQty': amount * price
            }
            ###

            net = self.bought[symbol]['cummulativeQuoteQty'] - \
                sell_market['cummulativeQuoteQty']
            print(f'Net profit: {net} USDT\n')

            self.bought[symbol] = None

        else:
            print(f"Not enough {symbol} to trade (minimum of $10)")

    def generateTicks(self):
        print('- Generating symbol step sizes...')
        try:
            ticks = openPickle('Ticks.pickle')
            print('- Loading ticks from file')
            self.ticks = ticks
        except Exception as ex:
            print(ex)
            for coin in markets:
                coin += 'USDT'
                self.getSymbolPrecision(coin)
            savePickle(self.ticks, 'Ticks.pickle')

    def getSymbolPrecision(self, symbol):
        for filt in self.client.get_symbol_info(symbol=symbol)['filters']:
            if filt['filterType'] == 'LOT_SIZE':
                diff = filt['stepSize'].find('1') - filt['stepSize'].find('.')
                self.ticks[symbol] = max(diff, 0)
                break

    def getKlines(self, symbol):
        raw_klines = self.client.get_klines(
            symbol=symbol, interval=tick_interval)
        return binanceToPandas(raw_klines)

    def refreshBalance(self):
        balance = self.client.get_account()["balances"]
        if balance is not None:
            self.available_currencies = []
            self.balance = []
            for dict in balance:
                dict["free"] = float(dict["free"])
                dict["locked"] = float(dict["locked"])

                if dict['asset'] == 'USDT':
                    self.usdt = float(dict["free"])
                elif (dict["free"] > 0.0):
                    dict["asset"] = dict["asset"]
                    self.available_currencies.append(dict["asset"])
                    self.balance.append(dict)
