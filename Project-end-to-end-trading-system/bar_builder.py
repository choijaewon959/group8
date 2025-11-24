import pandas as pd

class LiveBarBuilder:
    """
        Builds live OHLC bars from real time trade data.
        This is only used for Alpaca streaming data which provides tick-level trades. (paper trading)   
    """
    def __init__(self, interval="1min"):
        self.interval = pd.Timedelta(interval)  # e.g. "1min", "5s", etc.
        self.current_bar = None
        self.current_period_start = None

    def update(self, price, ts):
        # Convert timestamp to pandas Timestamp and floor to interval boundary
        ts = pd.Timestamp(ts).floor(self.interval)

        # First tick -> initialize bar
        if self.current_period_start is None:
            self.current_period_start = ts
            self.current_bar = {
                "timestamp": ts,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
            }
            return None

        # Same period -> update OHLC
        if ts == self.current_period_start:
            self.current_bar["high"] = max(self.current_bar["high"], price)
            self.current_bar["low"] = min(self.current_bar["low"], price)
            self.current_bar["close"] = price
            return None

        # New period -> close previous bar, start a new one
        completed_bar = self.current_bar

        self.current_period_start = ts
        self.current_bar = {
            "timestamp": ts,
            "open": price,
            "high": price,
            "low": price,
            "close": price,
        }

        return completed_bar