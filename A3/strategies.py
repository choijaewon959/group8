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

from functools import lru_cache

class MovingAverageStrategyMemo_LRUCache(Strategy):
    def __init__(self, window=60):
        self.window = window
        self.prices = []  # keep full history
        self.index = 0

    @staticmethod
    @lru_cache(maxsize=None)
    def prefix_sum(i, prices_tuple):
        if i <= 0:
            return 0
        return MovingAverageStrategyMemo_LRUCache.prefix_sum(i - 1, prices_tuple) + prices_tuple[i - 1]

    def generate_signals(self, tick):
        price = tick.price
        self.prices.append(price)
        self.index += 1

        if self.index < self.window:
            return None

        prices_tuple = tuple(self.prices)  # make it hashable
        psum = self.prefix_sum(self.index, prices_tuple)
        window_sum = psum - self.prefix_sum(self.index - self.window, prices_tuple)

        moving_avg = window_sum / self.window

        if price > moving_avg:
            return 1
        elif price < moving_avg:
            return -1
        return 0 

    def run(self, datapoints, tick_size):
        result = []
        for i in range(tick_size):
            signal = self.generate_signals(datapoints[i])
            result.append(signal)
        return result


# class NaiveMovingAverageStrategyOpti_Numpy(Strategy):
#     def __init__(self, window: int = 60):
#         self.__window = window

#     def generate_signals(self, datapoints, tick_size=1000) -> list:

#         m = min(len(datapoints), tick_size)
#         if m < self.__window:
#             return []

#         prices = np.array([dp.price for dp in datapoints[:m]], dtype=np.float32)
#         symbols = np.array([dp.symbol for dp in datapoints[:m]], dtype=object)
#         timestamps = np.array([dp.timestamp for dp in datapoints[:m]], dtype=object)

#         # using convolution for sliding window
#         window = self.__window
#         moving_avg = np.convolve(prices, np.ones(window)/window, mode='valid')

#         # datas will be used to calculate signals
#         ok_prices = prices[window-1:]
#         ok_symbols = symbols[window-1:]
#         ok_timestamps = timestamps[window-1:]

#         # vectorized calculation rather than calculate each tick
#         # np.sign() function will return -1/0/1 according to calculation result.
#         # ex) if price - moving_avg > 0 than return 1
#         positions_num = np.sign(ok_prices - moving_avg).astype(int)
#         # ,ap numeric positions to strings : Numpy is much faster when using numeric rather than string
#         mapping = {1: "BUY", -1: "SELL", 0: "HOLD"}
#         positions = np.vectorize(mapping.get)(positions_num)

#         # Combine all into signals
#         signals_array = np.column_stack((ok_timestamps, positions, ok_symbols, np.ones_like(ok_prices), ok_prices))
#         signals = [tuple(row) for row in signals_array]

#         return signals


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
