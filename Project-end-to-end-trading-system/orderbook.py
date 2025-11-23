import heapq
import time

class Order:
    def __init__(self, order_id:str, side:str, price:float, qty:float, timestamp:str):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.qty = qty
        self.timestamp = timestamp


class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.order_map = {}


    def add_order(self, side, price, qty):
        timestamp = time.time()
        order_id = str(timestamp)

        self.order_map[order_id] = Order(order_id, side, price, qty, timestamp)

        if side == "BUY":
            heapq.heappush(self.bids, (-price, timestamp, self.order_map[order_id]))
        else:
            heapq.heappush(self.asks, (price, timestamp, self.order_map[order_id]))

        self.match()
        return order_id

    def match(self):
        trades = []

        while True:
            best_bid = self.best_bid()
            best_ask = self.best_ask()

            if not best_bid or not best_ask:
                break

            bid_price = -best_bid[0]
            ask_price = best_ask[0]

            if bid_price < ask_price:
                break

            bid_order = best_bid[2]
            ask_order = best_ask[2]

            traded_qty = min(bid_order.qty, ask_order.qty)
            trade_price = ask_price

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


    def cancel_order(self, id):
        if id in self.order_map:
            self.order_map[id].qty = 0
            del self.order_map[id]

    def modify_order(self, id, price, qty, strategy_name):
        if id not in self.order_map:
            return

        order = self.order_map[id]
        order.qty = 0

        new_id = self.add_order(order.side, price, qty, strategy_name)
        return new_id


    def best_bid(self):
        while self.bids and self.bids[0][2].qty == 0:
            heapq.heappop(self.bids)
        return self.bids[0] if self.bids else None


    def best_ask(self):
        while self.asks and self.asks[0][2].qty == 0:
            heapq.heappop(self.asks)
        return self.asks[0] if self.asks else None


"""
order_book = OrderBook()
order_book.add_order("BUY", 100,20, "Volatility")
order_book.add_order("SELL", 80,30, "Volatility")
print(order_book.bids)
print(order_book.asks)
"""

