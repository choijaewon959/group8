from abc import ABC, abstractmethod
from collections import deque
from functools import lru_cache
from typing import List
import numpy as np


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass

class NaiveMovingAverageStrategy(Strategy):
    '''
        Time Complexity: O(window) per tick. Because for each tick, we compute sum(self.__prices[-window:]).
        Space Complexity: total O(T). Because self.__prices stores all past prices (as requested) without deletion.
    '''

    # intentionally save all data to make inefficiency 
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = [] 

    def generate_signals(self, tick) -> list:
        self.__prices.append(tick.price)

        if len(self.__prices) >= self.__window:
            moving_avg = sum(self.__prices[-self.__window:]) / self.__window
            price = tick.price

            if price > moving_avg:
                signal = 1
            elif price < moving_avg:
                signal = -1
            else:
                signal = 0

            return (tick.timestamp, signal, tick.symbol, 1, price)

    def run(self, datapoints, tick_size=1000):
        signals = []
        for i in range(tick_size):
            tick = datapoints[i]
            signals.append(self.generate_signals(tick))
        return signals

    
class MovingAverageStrategyMemo_Array(Strategy):
    def __init__(self, window:int = 60):
        self.__window = window
        self.__prices = []
        self.__window_sum = 0.0
    
    def generate_signals(self, tick) -> list:
        price = tick.price 
        self.__prices.append(price)

        if len(self.__prices) < self.__window:
            self.__window_sum += price
            return 
        
        self.__window_sum += self.__prices[-1] - self.__prices[-self.__window]
        moving_avg = self.__window_sum  / self.__window

        if price > moving_avg:
            signal = 1
        elif price < moving_avg:
            signal = -1
        else:
            signal = 0

        return (tick.timestamp, signal, tick.symbol, 1, price)

    def run(self, datapoints, tick_size=1000):
        signals = []
        for i in range(tick_size):
            tick = datapoints[i]
            signals.append(self.generate_signals(tick))
        return signals


class MovingAverageStrategyMemo_LRUCache(Strategy):
    __prices = []

    def __init__(self, window=60):
        self.__window = window
        self.__index = 0

    @classmethod
    @lru_cache(maxsize=None)
    def prefix_sum(cls, i):
        if i <= 0:
            return 0
        return cls.prefix_sum(i - 1) + cls.__prices[i - 1]

    def generate_signals(self, tick):
        price = tick.price
        self.__prices.append(price)

        if len(self.__prices) < self.__window:
            return 

        psum = type(self).prefix_sum(self.__index)
        prev = self.__index - self.__window
        window_sum = psum - type(self).prefix_sum(prev)

        moving_avg = window_sum / self.__window

        if tick.price > moving_avg:
            signal = 1
        elif tick.price < moving_avg:
            signal = -1
        else:
            signal = 0

        return (tick.timestamp, signal, tick.symbol, 1, tick.price)

    def run(self, datapoints, tick_size):
        signals = []
        for i in range(tick_size):
            self.__index = i
            signals.append(self.generate_signals(datapoints[i]))
        return signals
            

class WindowedMovingAverageStrategy(Strategy):
    # Time Complexity: O(1) per tick : Because the moving average is updated incrementally without recalculation of the sum
    # Space Complexity: O(window) : Because self.__prices is a fixed-size deque with maxlen=window.
    
    # request 1: maintain a fixed-size buffer, using a queue 
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = deque(maxlen=window)
        self.__sum = 0.0

    # request 2: update average incrementally O(1)
    def generate_signals(self, tick):
        if len(self.__prices) == self.__window:
            oldest = self.__prices[0]
            self.__sum -= oldest

        self.__prices.append(tick.price)
        self.__sum += tick.price

        if len(self.__prices) == self.__window:
            moving_avg = self.__sum / self.__window
            price = tick.price

            if price > moving_avg:
                signal = 1
            elif price < moving_avg:
                signal = -1
            else:
                signal = 0

            return ((tick.timestamp, signal, tick.symbol, 1, price))
    
    def run(self, datapoints, tick_size):
        signals = []
        for i in range(tick_size):
            tick = datapoints[i]
            signals.append(self.generate_signals(tick))
        return signals
    
## Execution Sample Test
# data = load_data()
# signals = []
# naiveMA = NaiveMovingAverageStrategy(window = 60)
# windowMA = WindowedMovingAverageStrategy(window= 60)
# for tick in data:
#     signals.append(windowMA.generate_signals(tick))
# print(signals)
