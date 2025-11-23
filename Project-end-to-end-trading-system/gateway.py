from order_manager import OrderManager
from orderbook import OrderBook
class Gateway:
    def __init__(self):
        self.order_book = OrderBook()
        self.order_manager = OrderManager()
        # in order to remain log
        self.all_trades = []
        self.all_orders = []

    def stream_data(self, df, strategy):

        for ts, row in df.iterrows():
            # update strategy
            strategy.update_live_bar(row, ts)
            signal = strategy.generate_live_signal()

            order_id = None
            trades = []

            if signal.action in ("BUY", "SELL") and signal.qty > 0:

                ok, msg = self.order_manager.can_place_order(
                    side=signal.action,
                    price=signal.price,
                    qty=signal.qty
                )

                if ok:
                    # generate order 
                    order_id = self.order_book.add_order(
                        signal.action,
                        signal.price,
                        signal.qty
                    )

                    # order record for OrderManager
                    self.order_manager.register_order(
                        order_id,
                        signal.action,
                        signal.price,
                        signal.qty
                    )

                    # order record for Gateway
                    self.all_orders.append({
                        "timestamp": ts,
                        "order_id": order_id,
                        "side": signal.action,
                        "price": signal.price,
                        "qty": signal.qty
                    })

                    # match trade
                    trades = self.order_book.match()

                    if trades:
                        # trade(filled) record for OrderManager
                        self.order_manager.handle_fills(trades)

                        # trade(filled) record for Gateway
                        self.all_trades.extend(trades)

                else:
                    order_id = None

            yield {
                "timestamp": ts,
                "signal": signal,
                "order_id": order_id,
                "trades": trades
            }
