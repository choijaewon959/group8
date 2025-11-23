import json
import time
from order_manager import OrderManager
from order_book2 import OrderBook

class Gateway:
    def __init__(self, log_file="./logs/orders.log"):
        self.order_manager = OrderManager()
        self.orderbook = OrderBook()
        self.log_file = log_file

    def stream_data(self, df, strategy):
        """
        df: pandas DataFrame with OHLCV
        strategy: Strategy instance
        """
        for ts, row in df.iterrows():
            
            # 1. update data for strategy
            strategy.update_live_bar(row, ts=ts)

            # 2. generate singla from strategy
            signal = strategy.generate_live_signal()

            # 3. after check through order manager, convert signal to order
            order_id = self.process_signal(signal)

            # 4. check filled trades from order book
            trades = self.handle_trades()

            yield {
                "timestamp": ts,
                "signal": signal,
                "order_id": order_id,
                "trades": trades
            }

    def _log(self, event, data):
        entry = {
            "timestamp": time.time(),
            "event": event,
            "data": data
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def send_order(self, side, price, qty, strategy_name="STRAT"):
        # order_manager test 
        ok, msg = self.order_manager.can_place_order(side, price, qty)
       
        if not ok: # not possible order
            self._log("order_rejected", {
                "side": side, "price": price, "qty": qty, "reason": msg
            })
            return None
        # possible order
        self.order_manager.register_order()
    
        # register to orderbook
        order_id = self.orderbook.add_order(side, price, qty, strategy_name)
    
        # leave log
        self._log("order_sent", {
            "order_id": order_id,
            "side": side,
            "price": price,
            "qty": qty
        })

        return order_id

    def cancel_order(self, oid):
        self.orderbook.cancel_order(oid)
        self._log("order_cancelled", {"order_id": oid})

    def modify_order(self, oid, new_price, new_qty):
        new_id = self.orderbook.modify_order(oid, new_price, new_qty)
        self._log("order_modified", {
            "old_id": oid,
            "new_id": new_id
        })
        return new_id

    def handle_trades(self):
        trades = self.orderbook.match()

        for t in trades:
            # buy side
            self.order_manager.update_after_fill(
                "BUY", t["price"], t["qty"]
            )
            # sell side
            self.order_manager.update_after_fill(
                "SELL", t["price"], t["qty"]
            )

            self._log("trade", t)

        return trades

    def process_signal(self, signal):
        if signal.action == "HOLD" or signal.qty == 0:
            return None

        price = signal.price
        side = signal.action
        qty = signal.qty
        strategy = signal.strategy_name

        order_id = self.send_order(side, price, qty, strategy)
        return order_id
