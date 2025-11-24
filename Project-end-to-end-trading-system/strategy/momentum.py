from collections import deque
import numpy as np
from strategy.signal import Signal
from strategy.strategybase import StrategyBase

class MomentumStrategy(StrategyBase):
    def __init__(self, lookback=30, threshold=0.001, position_size=1):
        """
        position_size = minimum quantity (min order size)
        """
        super().__init__(position_size, strategy_name="Momentum")

        self.lookback = lookback
        self.threshold = threshold

        # Momentum rolling window
        self.window = deque(maxlen=lookback)

        self.current_ts = None
        self.current_price = None

    def update_live_bar(self, row, ts=None):
        self.current_ts = ts
        self.current_price = row["close"]

        self.window.append(self.current_price)

    # --------------------------------------------------
    # Dynamic position sizing logic
    # --------------------------------------------------
    def compute_dynamic_size(self):
        """
        Position size increases with stronger momentum.
        Minimum position size = self.position_size
        """
        if len(self.window) < self.lookback:
            return 0  # no trading yet

        current = self.window[-1]
        past = self.window[0]
        momentum = abs((current / past) - 1)

        # === position size scaling rule ===
        # quantity grows with momentum strength
        qty = int(momentum * 100)   # scaling factor
        qty = max(1, qty)           # minimum size = 1
        qty = qty * self.position_size  # ensure compatibility with engine

        return qty

    # --------------------------------------------------
    # Generate signal
    # --------------------------------------------------
    def generate_live_signal(self):
        if len(self.window) < self.lookback:
            return Signal("HOLD", 0, price=self.current_price,
                          timestamp=self.current_ts, strategy_name=self.strategy_name)

        current = self.window[-1]
        past    = self.window[0]   # lookback ticks ago
        momentum = (current / past) - 1

        # Compute dynamic qty
        qty = self.compute_dynamic_size()

        # threshold base signal generation
        if momentum > self.threshold:
            return Signal("BUY", qty, price=self.current_price,
                          timestamp=self.current_ts, strategy_name=self.strategy_name)

        if momentum < -self.threshold:
            return Signal("SELL", qty, price=self.current_price,
                          timestamp=self.current_ts, strategy_name=self.strategy_name)

        return Signal("HOLD", 0, price=self.current_price,
                      timestamp=self.current_ts, strategy_name=self.strategy_name)
