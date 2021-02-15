import pandas as pd
import numpy as np
import math
import pickle


def binanceToPandas(klines):
    klines = np.array(klines)
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


def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def savePickle(var, file_name):
    outfile = open(file_name, 'wb')
    pickle.dump(var, outfile)

    outfile.close()


def openPickle(file_name):
    outfile = open(file_name, 'rb')
    df = pickle.load(outfile)

    outfile.close()

    return df
