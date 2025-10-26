from abc import ABC, abstractmethod, abstractclassmethod
from models import MarketDataPoint
import os
import pandas as pd
from collections import deque
import numpy as np
from observers import *

class Strategy():
    def getData(self):

        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, 'strategy_params.json')

        df = pd.Series(data_path, typ='Series').to_frame().T

        row = df[MeanReversionStrategy]
        return MarketDataPoint(row['lookback_window'], row['threshold'])

    @abstractmethod
    def generate_signals(self):
        pass

class MeanReversionStrategy(Strategy):

    def __init__(self):
        self.__data = Strategy()
        self.__data = self.getData()["MeanReversionStrategy"]
        self.__threshold = self.__data["threshold"]
        self.__window = self.__data["lookback_window"]
        self.__prices = deque(maxlen=self.__window)

    @abstractmethod
    def generate_signals(self, tick:MarketDataPoint) -> tuple:

        self.__prices.append(tick.price)

        if len(self.__prices) < self.__window:
            return (tick.symbol, 0, tick.qty, tick.price, tick.name)

        mean_price = np.mean(self.__prices)

        if tick.price < mean_price * (1 - self.__threshold):
            return (tick.symbol, 1, tick.qty, tick.price, tick.name)
        elif tick.price > mean_price * (1 + self.__threshold):
            return (tick.symbol, -1, tick.qty, tick.price, tick.name)

        if signal !=0:
            self._notify(signal, tick.price)
            return (tick.symbol, 0, tick.qty, tick.price, tick.name)

class BreakoutStrategy(Strategy):

    def __init__(self):
        super.__init__()
        self.__data = Strategy()
        self.__data = self.getData()["BreakoutStrategy"]
        self.__threshold = self.__data["threshold"]
        self.__window = self.__data["lookback_window"]
        self.__prices = deque(maxlen=self.__window)

    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> tuple:
        self.__prices.append(tick.price)
        if len(self.__prices) < self.__window:
            return 0

        high = np.max(self.__prices)
        low = np.min(self.__prices)

        if tick.price > high * (1 + self.__threshold):
            signal = 1
        elif tick.price < low * (1 - self.__threshold):
            signal = -1

        if signal != 0:
            self.notify(signal, tick.price)

        return (tick.symbol, signal, tick.qty, tick.price, tick.name)


def run(strategy, price_series):
    print(f"Running the strategy {strategy.name}")
    for i,p in enumerate(price_series):
        s = strategy.generate_signals(p)
        print(f"Tick {i}: price {s.price} and signal {s.signal}")

