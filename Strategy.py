import talib


def strategyDecision(ema8, ema13, ema21, ema34, ema55, rsi, kFast):
    ema8 = ema8.iloc[-1]
    ema13 = ema13.iloc[-1]
    ema21 = ema21.iloc[-1]
    ema34 = ema34.iloc[-1]
    ema55 = ema55.iloc[-1]
    rsi = rsi.iloc[-1]
    kFast = kFast.iloc[-1]

    return strategyCalculator(ema8, ema13, ema21, ema34, ema55, rsi, kFast)


def strategyCalculator(ema8, ema13, ema21, ema34, ema55, rsi, kFast):

    # MOMENTUM
    longEmaCondition = ema8 > ema13 and ema13 > ema21 and ema21 > ema34 and ema34 > ema55
    exitLongEmaCondition = ema13 < ema55

    # RSI
    longRsiCondition = rsi < 70 and rsi > 40
    exitLongRsiCondition = rsi > 70

    # STOCHASTIC
    longStochasticCondition = kFast < 80
    exitLongStochasticCondition = kFast > 95

    # STRAT
    enterLongCondition = longEmaCondition and longRsiCondition and longStochasticCondition
    exitLongCondition = (
        exitLongEmaCondition or exitLongRsiCondition or exitLongStochasticCondition)

    return (enterLongCondition, exitLongCondition)


def calculateIndicators(klines):
    ema8 = talib.EMA(klines['Close'], timeperiod=8)
    ema13 = talib.EMA(klines['Close'], timeperiod=13)
    ema21 = talib.EMA(klines['Close'], timeperiod=21)
    ema34 = talib.EMA(klines['Close'], timeperiod=34)
    ema55 = talib.EMA(klines['Close'], timeperiod=55)

    # ----------
    #  OSCILLATORS
    # ----------

    rsi = talib.RSI(klines['Close'], timeperiod=14)

    # ----------
    #  STOCHASTIC
    # ----------

    kFast, dFast = talib.STOCHF(
        klines['High'], klines['Low'], klines['Close'],  fastk_period=14)

    return (ema8, ema13, ema21, ema34, ema55, rsi, kFast)
