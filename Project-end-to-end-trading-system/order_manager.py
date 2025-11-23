# order_manager.py
import time

class OrderManager:
    def __init__(
        self,
        initial_capital=100000,
        max_position=1000,
        max_orders_per_min=6000000,
    ):
        self.capital = initial_capital
        self.max_position = max_position
        self.max_orders_per_min = max_orders_per_min

        self.positions = 0
        self.order_timestamps = []

    def _clean_old_orders(self):
        now = time.time()
        self.order_timestamps = [t for t in self.order_timestamps if now - t < 60]

    def can_place_order(self, side, price, qty):
        self._clean_old_orders()

        if len(self.order_timestamps) >= self.max_orders_per_min:
            return False, "Too many orders per minute"

        new_position = self.positions + (qty if side == "BUY" else -qty)
        if abs(new_position) > self.max_position:
            return False, "Position limit exceeded"

        required = price * qty if side == "BUY" else 0
        if required > self.capital:
            return False, "Not enough capital"

        return True, "OK"

    def register_order(self):
        self.order_timestamps.append(time.time())

    def update_after_fill(self, side, price, qty):
        if side == "BUY":
            self.capital -= price * qty
            self.positions += qty
        else:
            self.capital += price * qty
            self.positions -= qty
