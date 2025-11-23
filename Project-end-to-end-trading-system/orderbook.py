import heapq
import time

class Order:
    order_id: int
    side: int
    price: float
    qty: float
    timestamp: float


class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.order_map = {}


    def add_order(self, side, price, qty, strategy_name):
        timestamp = time.time()
        order_id = str(timestamp) + strategy_name

        self.order_map[order_id] = Order(order_id, side, price, qty, timestamp)
        order = self.order_map[order_id]

        if side == "BUY":
            heapq.heappush(self.bids, (-price, timestamp, order))
        else:
            heapq.heappush(self.asks, (price, timestamp, order))

        self.match()
        return order_id


    def cancel_order(self, id):
        if id in self.order_map:
            self.order_map[id].qty = 0
            del self.order_map[id]

    def modify_order(self, id, price, qty):
        if id not in self.order_map:
            return

        order = self.order_map[id]
        order.qty = 0

        new_id = self.add_order(order.side, price, qty)
        return new_id


    def best_bid(self):
        while self.bids and self.bids[0][2].qty == 0:
            heapq.heappop(self.bids)
        return self.bids[0] if self.bids else None


    def best_ask(self):
        while self.asks and self.asks[0][2].qty == 0:
            heapq.heappop(self.asks)
        return self.asks[0] if self.asks else None


    def match(self):
        trades = []

        while True:
            bid = self.best_bid()
            ask = self.best_ask()

            if bid and ask:

                bid = bid[0]
                ask = ask[0]

                if bid < ask:
                    break

                bid_order = bid[2]
                ask_order = ask[2]

                traded_qty = min(bid_order.qty, ask_order.qty)
                trade_price = ask

                bid_order.qty -= traded_qty
                ask_order.qty -= traded_qty

                trades.append({
                "price": trade_price,
                "qty": traded_qty,
                "buy_id" : bid_order.order_id,
                "sell_id" : ask_order.order_id,
                "timestamp" : time.time()
                })

                if bid_order.qty == 0:
                    heapq.heappop(self.bids)
                    del self.order_map[bid_order.order_id]

                if ask_order.qty == 0:
                    heapq.heappop(self.asks)
                    del self.order_map[ask_order.order_id]

        return trades
