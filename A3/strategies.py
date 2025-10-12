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
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = [] 

    def generate_signals(self, datapoints, tick_size=600) -> list:
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
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = deque(maxlen=self.__window)

    @lru_cache(maxsize=None)
    #caching moving averages for a window of prices
    def computeAveragePrice(self, prices):
        return sum(prices) / len(prices)

    def generate_signals(self, datapoints, tick_size=600) -> list:
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
    
class NaiveMovingAverageStrategyOptiMemo2(Strategy):
    def __init__(self, window:int = 60):
        self.__window = window
    
    def generate_signals(self, datapoints, tick_size=600) -> list:
        signals = []
        window_sum = sum(dp.price for dp in datapoints[:self.__window])  # initial window

        for i in range(self.__window, tick_size):
            window_sum += datapoints[i].price - datapoints[i - self.__window].price
            moving_avg = window_sum / self.__window
            tick = datapoints[i]

            if tick.price > moving_avg:
                signal = "BUY"
            elif tick.price < moving_avg:
                signal = "SELL"
            else:
                signal = "HOLD"

            signals.append((tick.timestamp, signal, tick.symbol, 1, tick.price))

        return signals

class NaiveMovingAverageStrategyOptiMemo3(Strategy):
    def __init__(self, window=60):
        self.__window = window

    def generate_signals(self, datapoints, tick_size=600):
        signals = []

        @lru_cache(maxsize=self.__window*2)
        def prefix_sum(i):
            if i == 0:
                return 0
            return prefix_sum(i - 1) + datapoints[i - 1].price

        for i in range(self.__window, tick_size):
            # window sum using cached prefix sums
            # cached window sum upto index i - cached sum upto i - window
            psum = prefix_sum(i)
            prev = i - self.__window
            window_sum = psum - prefix_sum(prev)

            moving_avg = window_sum / self.__window
            tick = datapoints[i]

            if tick.price > moving_avg:
                signal = "BUY"
            elif tick.price < moving_avg:
                signal = "SELL"
            else:
                signal = "HOLD"

            signals.append((tick.timestamp, signal, tick.symbol, 1, tick.price))

        return signals


class NaiveMovingAverageStrategyOpti_Numpy(Strategy):
    def __init__(self, window: int = 60):
        self.__window = window

    def generate_signals(self, datapoints, tick_size=600) -> list:

        m = min(len(datapoints), tick_size)
        if m < self.__window:
            return []

        prices = np.array([dp.price for dp in datapoints[:m]], dtype=np.float32)
        symbols = np.array([dp.symbol for dp in datapoints[:m]], dtype=object)
        timestamps = np.array([dp.timestamp for dp in datapoints[:m]], dtype=object)

        # using convolution for sliding window
        window = self.__window
        moving_avg = np.convolve(prices, np.ones(window)/window, mode='valid')

        # datas will be used to calculate signals
        ok_prices = prices[window-1:]
        ok_symbols = symbols[window-1:]
        ok_timestamps = timestamps[window-1:]

        # vectorized calculation rather than calculate each tick
        # np.sign() function will return -1/0/1 according to calculation result.
        # ex) if price - moving_avg > 0 than return 1
        positions_num = np.sign(ok_prices - moving_avg).astype(int)
        # ,ap numeric positions to strings : Numpy is much faster when using numeric rather than string
        mapping = {1: "BUY", -1: "SELL", 0: "HOLD"}
        positions = np.vectorize(mapping.get)(positions_num)

        # Combine all into signals
        signals_array = np.column_stack((ok_timestamps, positions, ok_symbols, np.ones_like(ok_prices), ok_prices))
        signals = [tuple(row) for row in signals_array]

        return signals


class NaiveMovingAverageStrategyOpti_generator(Strategy):
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = []

    def generate_signals(self, datapoints, tick_size=600) -> list:
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
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = deque(maxlen=window)
        self.__sum = 0.0

    # request 2: update average incrementally O(1)
    def generate_signals(self, datapoints, tick_size=600) -> list:
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
    
    def __init__(self, window: int = 60):
        self.window = window
        self.prices = deque(maxlen=window)
        self.avg = 0.0  # current moving average

    def generate_signals(self, datapoints, tick_size=600) -> List:
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
# naiveMA = NaiveMovingAverageStrategy(window = 60)
# windowMA = WindowedMovingAverageStrategy(window= 60)
# for tick in data:
#     signals.append(windowMA.generate_signals(tick))
# print(signals)
