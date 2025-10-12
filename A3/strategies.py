from abc import ABC, abstractmethod
from collections import deque
from functools import lru_cache
from unittest import signals
from typing import List
from datetime import datetime
import numpy as np


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass

class NaiveMovingAverageStrategy(Strategy):
    # Time Complexity: O(window) per tick. Because for each tick, we compute sum(self.__prices[-window:]).
    # Space Complexity: total O(T). Because self.__prices stores all past prices (as requested) without deletion.
    
    # intentionally save all data to make inefficiency 
    def __init__(self, window: int = 20):
        self.__window = window
        self.__prices = [] 

    def generate_signals(self, datapoints, tick_size=1000) -> list:
        signals = []
        for tick in datapoints[:tick_size]:  # process only up to tick_size data points
            self.__prices.append(tick.price)

            if len(self.__prices) >= self.__window:
                moving_avg = sum(self.__prices[-self.__window:]) / self.__window
                price = tick.price

                if price > moving_avg:
                    signals.append((tick.timestamp, "BUY", tick.symbol, 1, price))
                elif price < moving_avg:
                    signals.append((tick.timestamp, "SELL", tick.symbol, 1, price))
                else:
                    signals.append((tick.timestamp, "HOLD", tick.symbol, 1, price))
        return signals

class NaiveMovingAverageStrategyOpti_memo(Strategy):
    def __init__(self, window: int = 20):
        self.__window = window
        self.__prices = deque(maxlen=self.__window)

    @lru_cache(maxsize=None)
    #caching moving averages for a window of prices
    def computeAveragePrice(self, prices):
        return sum(prices) / len(prices)

    def generate_signals(self, datapoints, tick_size=1000) -> list:
        signals = []

        for tick in datapoints[:tick_size]:  # process only up to tick_size data points
            if len(self.__prices) >= self.__window:
                self.__prices.popleft()

            self.__prices.append(tick.price)

            if len(self.__prices) >= self.__window:
                moving_avg = self.computeAveragePrice(tuple(self.__prices))
                price = tick.price

                if price > moving_avg:
                    signals.append((tick.timestamp, "BUY", tick.symbol, 1, price))
                elif price < moving_avg:
                    signals.append((tick.timestamp, "SELL", tick.symbol, 1, price))
                else:
                    signals.append((tick.timestamp, "HOLD", tick.symbol, 1, price))
        return signals


class NaiveMovingAverageStrategyOpti_Numpy(Strategy):
    def __init__(self, window: int = 20):
        self.__window = window

    def generate_signals(self, datapoints, tick_size=1000) -> list:
        m=min(len(datapoints), tick_size)
        if m < self.__window:
            return []
        prices = np.empty(m, dtype=np.float32)
        symbols = np.empty(m, dtype=object)
        timestamps = np.empty(m, object)

        for i in range(m):
            prices[i]=datapoints[i].price
            symbols[i] = datapoints[i].symbol
            timestamps[i] = datapoints[i].timestamp

        cs = np.add.accumulate(prices)
        prefix = np.zeros_like(cs)
        prefix[self.__window:] = cs[:-self.__window]
        moving_avg = (cs - prefix)[self.__window - 1:] / self.__window

        ok_prices = prices[self.__window-1:]
        ok_symbols = symbols[self.__window-1:]
        ok_timestamps = timestamps[self.__window-1:]

        positions = np.where(ok_prices > moving_avg, "BUY",
                  np.where(ok_prices < moving_avg, "SELL", "HOLD"))

        signals = [(t, sig, sym, 1, pr) for (t, sig, sym, pr) in zip(ok_timestamps, positions, ok_symbols, ok_prices)]

        return signals

class NaiveMovingAverageStrategyOpti_generator(Strategy):
    def __init__(self, window: int = 20):
        self.__window = window
        self.__prices = []

    def generate_signals(self, datapoints, tick_size=1000) -> list:
        signals = []

        for data in datapoints[:tick_size]:
            price = data.price
            self.__prices.append(price)

            if len(self.__prices) >= self.__window:
                moving_avg = self.__prices[-self.__window:] / len(self.__prices)

                if price > moving_avg:
                    signals.append((data.timestamp, "BUY", data.symbol, 1, price))
                elif price < moving_avg:
                    signals.append((data.timestamp, "SELL", data.symbol, 1, price))
                else:
                    signals.append((data.timestamp, "HOLD", data.symbol, 1, price))

                yield signals




class WindowedMovingAverageStrategy(Strategy):
    # Time Complexity: O(1) per tick : Because the moving average is updated incrementally without recalculation of the sum
    # Space Complexity: O(window) : Because self.__prices is a fixed-size deque with maxlen=window.
    
    # request 1: maintain a fixed-size buffer, using a queue 
    def __init__(self, window: int = 20):
        self.__window = window
        self.__prices = deque(maxlen=window)
        self.__sum = 0.0

    # request 2: update average incrementally O(1)
    def generate_signals(self, datapoints, tick_size=1000) -> list:
        signals = []
        for tick in datapoints[:tick_size]:
            if len(self.__prices) == self.__window:
                oldest = self.__prices[0]
                self.__sum -= oldest

            self.__prices.append(tick.price)
            self.__sum += tick.price

            if len(self.__prices) == self.__window:
                moving_avg = self.__sum / self.__window
                price = tick.price

                if price > moving_avg:
                    signals.append((tick.timestamp, "BUY", tick.symbol, 1, price))
                elif price < moving_avg:
                    signals.append((tick.timestamp, "SELL", tick.symbol, 1, price))
                else:
                    signals.append((tick.timestamp, "HOLD", tick.symbol, 1, price))
        return signals
    



class WindowedMovingAverageStrategy_Opt(Strategy):
    # Time: O(1) per tick (incremental update)
    # Space: O(window) (deque only)
    
    def __init__(self, window: int = 20):
        self.window = window
        self.prices = deque(maxlen=window)
        self.avg = 0.0  # current moving average

    def generate_signals(self, datapoints, tick_size=1000) -> List:
        signals = []

        for tick in datapoints[:tick_size]:
            # Remove oldest price if deque full
            removed = 0.0
            if len(self.prices) == self.window:
                removed = self.prices.popleft()
            self.prices.append(tick.price)

            # Incremental moving average
            k = len(self.prices)
            self.avg = self.avg + (tick.price - removed) / k

            # Generate signal only when window is full
            if k == self.window:
                if tick.price > self.avg:
                    signals.append((tick.timestamp, "BUY", tick.symbol, 1, tick.price))
                elif tick.price < self.avg:
                    signals.append((tick.timestamp, "SELL", tick.symbol, 1, tick.price))
                else:
                    signals.append((tick.timestamp, "HOLD", tick.symbol, 1, tick.price))

        return signals

## Execution Sample Test
# data = load_data()
# signals = []
# naiveMA = NaiveMovingAverageStrategy(window = 20)
# windowMA = WindowedMovingAverageStrategy(window= 20)
# for tick in data:
#     signals.append(windowMA.generate_signals(tick))
# print(signals)
