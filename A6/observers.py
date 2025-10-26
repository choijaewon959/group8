from collections import deque
import numpy as np
from strategies import BreakoutStrategy

class SignalPublisher():
    def __init__(self):
        self.__observers=[]

    def update(self, callblack):
        self.__observers.append(callblack)

    def _notify(self, signal, price):
        for callback in self.__observers:
            callback(signal, price, strategy=self.__class__.__name__)

def broker_listener(signal, price, strategy):
    side = 1 if signal > 0 else -1
    print(f"[BROKER] {strategy} -> {side} at price {price}")

def logger_listener(signal, price, strategy):
    print(f"[LOGGER] {strategy} emits signal {signal} at {price} ")


observers = SignalPublisher()

observers.attach(broker_listener)
observers.attach(logger_listener)

breakout = BreakoutStrategy()
run(breakout, price_series)









