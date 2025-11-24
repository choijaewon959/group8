from collections import deque
import numpy as np
from strategy.signal import Signal
from strategy.strategybase import StrategyBase

class MomentumStrategy(StrategyBase):
    def __init__(self, lookback=30, threshold=0.001, position_size=1):
        super().__init__(position_size, strategy_name="Momentum")

        self.lookback = lookback
        self.threshold = threshold

        # Rolling window for momentum
        self.window = deque(maxlen=lookback)

        self.current_ts = None
        self.current_price = None   

    def update_live_bar(self, row, ts=None):
        self.current_ts = ts
        self.current_price = row["close"]   
        self.window.append(self.current_price)

    def generate_live_signal(self):
        if len(self.window) < self.lookback:
            return Signal(
                "HOLD", 
                0,
                price=self.current_price,      
                timestamp=self.current_ts,
                strategy_name=self.strategy_name
            )

        current = self.window[-1]
        past    = self.window[0]
        momentum = (current / past) - 1   

        # --------------------------------------------------
        # Dynamic position sizing logic
        # --------------------------------------------------
        raw_size = abs(momentum) * 1000
        dynamic_qty = max(1, int(raw_size))
        dynamic_qty = dynamic_qty * self.position_size 

        # ------------------------------
        # BUY
        # ------------------------------
        if momentum > self.threshold:
            return Signal(
                "BUY", 
                dynamic_qty,
                price=current,                
                timestamp=self.current_ts,
                strategy_name=self.strategy_name
            )

        # ------------------------------
        # SELL
        # ------------------------------
        if momentum < -self.threshold:
            return Signal(
                "SELL", 
                dynamic_qty,
                price=current,                
                timestamp=self.current_ts,
                strategy_name=self.strategy_name
            )

        # ------------------------------
        # HOLD
        # ------------------------------
        return Signal(
            
            "HOLD", 
            0,
            price=current,                   
            timestamp=self.current_ts,
            strategy_name=self.strategy_name
        )
