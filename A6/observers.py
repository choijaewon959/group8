from collections import deque
import numpy as np

class Observer():
    def update(self, signal:dict):
        pass

class SignalPublisher():
    def __init__(self):
        self.__observers=[]

    def attach(self, observer: Observer):
        self.__observers.append(observer)

    def notify(self, signal: dict):
        for observer in self.__observers:
            observer.update(signal)


class LoggerObserver(Observer):
    def update(self, signal):
        print(f"[LOGGER] {signal['strategy']} emits signal {signal['signal']} at {signal['price']} on {signal['symbol']}")

class AlertObserver(Observer):
    def update(self, signal):
        if abs(signal['signal']) == 1 and signal['qty']> 1:
            print(f"[ALERT] LARGE TRADE involving {signal['strategy']}: emits {signal['signal']} signal for {signal['qty']} units at {signal['price']} ")



"""
observers = SignalPublisher()

observers.attach(broker_listener)
observers.attach(logger_listener)

breakout = BreakoutStrategy()
run(breakout, price_series)
"""









