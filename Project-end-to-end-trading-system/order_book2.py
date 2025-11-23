import heapq
import time


class Order:
    def __init__(self, order_id, side, price, qty, timestamp):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.qty = qty
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class OrderBook:
    def __init__(self):
        self.bids = []  # max-heap 
        self.asks = []  # min-heap
        self.order_map = {}  

    def add_order(self, side, price, qty, strategy_name):
        timestamp = time.time()
        order_id = f"{timestamp}{strategy_name}"

        order = Order(order_id, side, price, qty, timestamp)
        self.order_map[order_id] = order

        if side == "BUY":
            heapq.heappush(self.bids, (-price, timestamp, order))
        else:
            heapq.heappush(self.asks, (price, timestamp, order))

        return order_id

    def cancel_order(self, oid):
        if oid in self.order_map:
            self.order_map[oid].qty = 0  
            del self.order_map[oid]

    def modify_order(self, oid, new_price, new_qty):
        if oid not in self.order_map:
            return None

        old_order = self.order_map[oid]
        old_order.qty = 0
        del self.order_map[oid]

        return self.add_order(old_order.side, new_price, new_qty, "MOD")

    def best_bid(self):
        while self.bids:
            _, _, order = self.bids[0]
            if order.order_id in self.order_map and order.qty > 0:
                return self.bids[0]
            heapq.heappop(self.bids)
        return None

    def best_ask(self):
        while self.asks:
            _, _, order = self.asks[0]
            if order.order_id in self.order_map and order.qty > 0:
                return self.asks[0]
            heapq.heappop(self.asks)
        return None

    def match(self):
        trades = []

        while True:
            bid_tuple = self.best_bid()
            ask_tuple = self.best_ask()

            if not bid_tuple or not ask_tuple:
                break

            bid_price, bid_ts, bid_order = bid_tuple
            ask_price, ask_ts, ask_order = ask_tuple

            bid_price = -bid_price

            if bid_price < ask_price:
                break

            traded_qty = min(bid_order.qty, ask_order.qty)
            trade_price = ask_price  

            bid_order.qty -= traded_qty
            ask_order.qty -= traded_qty

            trades.append({
                "price": trade_price,
                "qty": traded_qty,
                "buy_id": bid_order.order_id,
                "sell_id": ask_order.order_id,
                "timestamp": time.time()
            })

            if bid_order.qty == 0:
                heapq.heappop(self.bids)
                if bid_order.order_id in self.order_map:
                    del self.order_map[bid_order.order_id]

            if ask_order.qty == 0:
                heapq.heappop(self.asks)
                if ask_order.order_id in self.order_map:
                    del self.order_map[ask_order.order_id]

        return trades
