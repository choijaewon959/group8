from collections import deque
import numpy as np
from strategy.signal import Signal
from strategy.strategybase import StrategyBase

class MACrossStrategy(StrategyBase):
    def __init__(self, short_window=20, long_window=60, position_size=1):
        super().__init__(position_size, strategy_name="MACross")
        self.short_window = short_window
        self.long_window  = long_window

        # rolling window deque
        self.short_q = deque(maxlen=short_window)
        self.long_q  = deque(maxlen=long_window)

        self.current_ts = None

    def update_live_bar(self, row, ts=None):
        self.current_ts = ts
        price = row["Close"]

        self.short_q.append(price)
        self.long_q.append(price)

    def generate_live_signal(self):
        # not enough data
        if len(self.short_q) < self.short_window or len(self.long_q) < self.long_window:
            return Signal("HOLD", 0, timestamp=self.current_ts, strategy_name=self.strategy_name)

        ma_s = np.mean(self.short_q)
        ma_l = np.mean(self.long_q)

        if ma_s > ma_l:
            return Signal("BUY", self.position_size, timestamp=self.current_ts, strategy_name=self.strategy_name)

        if ma_s < ma_l:
            return Signal("SELL", self.position_size, timestamp=self.current_ts, strategy_name=self.strategy_name)

        return Signal("HOLD", 0, timestamp=self.current_ts, strategy_name=self.strategy_name)
