from abc import ABC, abstractmethod, abstractclassmethod

from models import MarketDataPoint
import os
import pandas as pd
from collections import deque
import numpy as np
from observers import *

class Strategy(ABC):
    def __init__(self, params, publisher):
        self.params = params
        self.publisher = publisher

    @abstractmethod
    def generate_signals(self):
        pass

class MeanReversionStrategy(Strategy):

    def __init__(self, params, publisher):
        super().__init__(params, publisher)
        self.__threshold = params["threshold"]
        self.__window = params["lookback_window"]
        self.__prices = deque(maxlen=self.__window)

    def generate_signals(self, tick: MarketDataPoint) -> dict:

        self.__prices.append(tick.price)
        signal = 0

        if len(self.__prices) < self.__window:
            return 0

        mean_price = np.mean(self.__prices)

        if tick.price < mean_price * (1 - self.__threshold):
            signal = 1
        elif tick.price > mean_price * (1 + self.__threshold):
            signal = -1

        if signal !=0:
            signal_data = {'strategy': "MeanReversionStrategy",
                           'symbol': tick.symbol,
                           'signal': signal,
                           'price': tick.price,
                           'qty': 2,
                           }
            self.publisher.notify(signal_data)
            return signal_data

class BreakoutStrategy(Strategy):

    def __init__(self, params, publisher):
        super().__init__(params, publisher)
        self.__threshold = params["threshold"]
        self.__window = params["lookback_window"]
        self.__prices = deque(maxlen=self.__window)

    def generate_signals(self, tick: MarketDataPoint) -> dict:

        self.__prices.append(tick.price)
        signal = 0
        
        if len(self.__prices) < self.__window:
            return 0

        high = np.max(self.__prices)
        low = np.min(self.__prices)

        if tick.price > high * (1 + self.__threshold):
            signal = 1
        elif tick.price < low * (1 - self.__threshold):
            signal = -1

        if signal != 0:
            signal_data = {'strategy': "MeanReversionStrategy",
                           'symbol': tick.symbol,
                           'signal': signal,
                           'price': tick.price,
                           'qty': 2,
                           }
            self.publisher.notify(signal_data)

            return signal_data
