from abc import ABC, abstractmethod
from collections import deque
from functools import lru_cache

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass

class NaiveMovingAverageStrategy(Strategy):
    '''
        Time Complexity: O(k) per tick where k is window size. Because for each tick, we compute sum(self.__prices[-window:]).
        Space Complexity: total O(N). Because self.__prices stores all past prices without deletion.
    '''
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = [] 
        
    def generate_signals(self, tick) -> list:
        self.__prices.append(tick.price)

        if len(self.__prices) >= self.__window:
            # re-calculating moving average for predefined window.
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
        for i in range(min(len(datapoints), tick_size)):
            tick = datapoints[i]
            signals.append(self.generate_signals(tick))
        return signals

class MovingAverageStrategyMemo_Array(Strategy):
    '''
        Time Complexity: O(1) per tick. we directly access to prices using index and index - window size.
        Space Complexity: total O(N). Because self.__prices stores all past prices without deletion.
    '''
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
        
        # only updating window sum, without re-calculating total sum of elements everytime
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
        for i in range(min(len(datapoints), tick_size)):
            tick = datapoints[i]
            signals.append(self.generate_signals(tick))
        return signals


class MovingAverageStrategyMemo_LRUCache(Strategy):
    '''
        Time Complexity: O(1) per tick. we directly access to prices using index and index - window size.
        Space Complexity: total O(N). Because self.__prices stores all past prices without deletion.
    '''
    def __init__(self, window=60):
        self.__window = window
        self.__moving_avg = 0.0

    def generate_signals(self, tick):
        if tick.price > self.__moving_avg:
            signal = 1
        elif tick.price < self.__moving_avg:
            signal = -1
        else:
            signal = 0
        return (tick.timestamp, signal, tick.symbol, 1, tick.price)

    def run(self, datapoints, tick_size):
        signals = []

        # Caching the prefix_sum output based on index variable.
        @lru_cache(maxsize=None)
        def prefix_sum(i):
            if i == 0:
                return 0
            return prefix_sum(i - 1) + datapoints[i - 1].price

        for i in range(self.__window, min(len(datapoints), tick_size)):
            psum = prefix_sum(i)
            prev = i - self.__window
            window_sum = psum - prefix_sum(prev)

            self.__moving_avg = window_sum / self.__window
            signals.append(self.generate_signals(datapoints[i]))
        return signals

class WindowedMovingAverageStrategy(Strategy):
    '''
        Time Complexity: O(1) per tick : Because the moving average is updated incrementally without recalculation of the sum.
        Space Complexity: O(window) : Because self.__prices is a fixed-size deque with maxlen=window.
    '''
    # maintain a fixed-size buffer, using a queue 
    def __init__(self, window: int = 60):
        self.__window = window
        self.__prices = deque(maxlen=window)
        self.__sum = 0.0

    # update average incrementally O(1)
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
            return (tick.timestamp, signal, tick.symbol, 1, price)
    
    def run(self, datapoints, tick_size):
        signals = []
        for i in range(min(len(datapoints), tick_size)):
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
