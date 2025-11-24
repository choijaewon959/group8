from collections import deque
import numpy as np
from strategy.signal import Signal
from strategy.strategybase import StrategyBase


class MACrossStrategy(StrategyBase):
    def __init__(self, short_window=20, long_window=60, position_size=1):
        """
        position_size = minimum quantity (min order size)
        """
        super().__init__(position_size, strategy_name="MACross")

        self.short_window = short_window
        self.long_window  = long_window

        # queues for moving averages
        self.short_q = deque(maxlen=short_window)
        self.long_q  = deque(maxlen=long_window)

        self.current_ts = None
        self.current_price = None

    # --------------------------------------------------
    # Update new price bar
    # --------------------------------------------------
    def update_live_bar(self, row, ts=None):
        self.current_ts = ts
        self.current_price = row["close"]

        self.short_q.append(self.current_price)
        self.long_q.append(self.current_price)

    # --------------------------------------------------
    # Dynamic position sizing logic
    # --------------------------------------------------
    def compute_dynamic_size(self):
        """
        Position size increases when short MA and long MA diverge more.
        Minimum position size = self.position_size
        """
        if len(self.short_q) < self.short_window or len(self.long_q) < self.long_window:
            return 0  # no trading yet

        ma_s = np.mean(self.short_q)
        ma_l = np.mean(self.long_q)

        diff = abs(ma_s - ma_l)

        # === position size scaling rule ===
        # quantity grows with MA distance
        qty = int(diff * 5)         # scaling factor
        qty = max(1, qty)           # minimum size = 1
        qty = qty * self.position_size  # ensure compatibility with engine

        return qty

    # --------------------------------------------------
    # Generate signal
    # --------------------------------------------------
    def generate_live_signal(self):
        # Not enough data yet
        if len(self.short_q) < self.short_window or len(self.long_q) < self.long_window:
            return Signal("HOLD", 0, price=self.current_price,
                          timestamp=self.current_ts, strategy_name=self.strategy_name)

        ma_s = np.mean(self.short_q)
        ma_l = np.mean(self.long_q)

        # Compute dynamic qty
        qty = self.compute_dynamic_size()
        print("@@@@@@@@@@@@@@@@@@@@", ma_s, ma_l, qty)

        if ma_s > ma_l:
            return Signal("BUY", qty, price=self.current_price,
                          timestamp=self.current_ts, strategy_name=self.strategy_name)

        if ma_s < ma_l:
            return Signal("SELL", qty, price=self.current_price,
                          timestamp=self.current_ts, strategy_name=self.strategy_name)

        return Signal("HOLD", 0, price=self.current_price,
                      timestamp=self.current_ts, strategy_name=self.strategy_name)
