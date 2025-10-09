from abc import ABC, abstractmethod
from collections import deque
from data_loader import load_data # only for test

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass

class NaiveMovingAverageStrategy(Strategy):
    # intentionally save all data to make inefficiency 
    def __init__(self, window: int = 20):
        self.__window = window
        self.__prices = [] 

    def generate_signals(self, tick) -> list:
        self.__prices.append(tick.price)
        signals = []

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

class WindowedMovingAverageStrategy(Strategy):
    # request 1: maintain a fixed-size buffer, using a queue 
    def __init__(self, window: int = 20):
        self.__window = window
        self.__prices = deque(maxlen=window)
        self.__sum = 0.0

    # request 2: update average incrementally O(1)
    def generate_signals(self, tick) -> list:
        signals = []

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
    


## Execution Sample Test
# data = load_data()
# signals = []
# naiveMA = NaiveMovingAverageStrategy(window = 20)
# windowMA = WindowedMovingAverageStrategy(window= 20)
# for tick in data:
#     signals.append(windowMA.generate_signals(tick))
# print(signals)
