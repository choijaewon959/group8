import time
from orderbook import OrderBook

class OrderManager:
    def __init__(
        self,
        initial_capital=100000,
        max_position=1000,
        max_orders_per_min=10000,
    ):
        self.capital = initial_capital
        self.max_position = max_position
        self.max_orders_per_min = max_orders_per_min

        self.positions = 0
        self.order_timestamps = []

        self.active_orders = {}

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

        return True

    def register_order(self, order_id, side, price, qty):
        self.order_timestamps.append(time.time())
        self.active_orders[order_id] = {
            "side": side,
            "price": price,
            "qty": qty,
            "filled": 0
        }

    def send_order(self, order_book, side, price, qty):
        allowed = self.can_place_order(side, price, qty)
        if not allowed:
            return None

        order_id = order_book.add_order(side, price, qty)

        self.register_order(order_id, side, price, qty)

        return order_id, "ORDER_ACCEPTED"

    def handle_fills(self, trades):
        for trade in trades:
            for role in ["buy_id", "sell_id"]:
                oid = trade.get(role)
                if oid in self.active_orders:
                    side = self.active_orders[oid]["side"]
                    qty = trade["qty"]
                    price = trade["price"]

                    self.active_orders[oid]["filled"] += qty

                    if side == "BUY":
                        self.capital -= price * qty
                        self.positions += qty
                    else:
                        self.capital += price * qty
                        self.positions -= qty

                    if self.active_orders[oid]["filled"] == self.active_orders[oid]["qty"]:
                        del self.active_orders[oid]


ob = OrderBook()
om = OrderManager()

order_id, status = om.send_order(ob, "BUY", 100, 10)
order_id, status = om.send_order(ob, "SELL", 90, 10)
print(order_id, status)

trades = ob.match()

om.handle_fills(trades)

print("Capital:", om.capital)
print("Positions:", om.positions)