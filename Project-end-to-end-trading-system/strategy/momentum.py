from collections import deque
import numpy as np
from strategy.signal import Signal
from strategy.strategybase import StrategyBase

class MomentumStrategy(StrategyBase):
    def __init__(self, lookback=30, threshold=0.001, position_size=1):
        super().__init__(position_size, strategy_name="Momentum")

        self.lookback = lookback
        self.threshold = threshold

        # Momentum rolling window
        self.window = deque(maxlen=lookback)

        self.current_ts = None

    def update_live_bar(self, row, ts=None):
        self.current_ts = ts
        price = row["Close"]

        self.window.append(price)

    def generate_live_signal(self):
        if len(self.window) < self.lookback:
            return Signal("HOLD", 0, timestamp=self.current_ts, strategy_name=self.strategy_name)

        current = self.window[-1]
        past    = self.window[0]   # lookback ticks ago
        momentum = (current / past) - 1

        # threshold base signal generation
        if momentum > self.threshold:
            return Signal("BUY", self.position_size, timestamp=self.current_ts, strategy_name=self.strategy_name)

        if momentum < -self.threshold:
            return Signal("SELL", self.position_size, timestamp=self.current_ts, strategy_name=self.strategy_name)

        return Signal("HOLD", 0, timestamp=self.current_ts, strategy_name=self.strategy_name)
