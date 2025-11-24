import os
import pandas as pd
from gateway import Gateway
from strategy.ma_cross import MACrossStrategy


class Engine:
    def __init__(self, gateway, strategy):
        """
        Initialize the Engine.

        gateway : Gateway instance that manages data feed and order handling
        strategy : Strategy instance that generates trading signals
        """
        self.gateway = gateway
        self.strategy = strategy
        self.all_events = []        # Store all events received from the Gateway
        self.all_trades = []        # Store all accumulated trades

    def run(self, df):
        """
        Run the main backtesting loop.

        df : pandas DataFrame representing historical intraday data
        """
        print("=== Engine Run Start ===\n")

        for event in self.gateway.stream_data(df, self.strategy):

            # Collect filled trades
            if event["trades"]:
                self.all_trades.extend(event["trades"])

            # Log all events
            self.all_events.append(event)

            # Print monitoring information to console
            self.print_event(event)

        print("\n=== Engine Run Complete ===")
        print(f"Total Trades Executed : {len(self.all_trades)}")
        print(f"Total Events Processed: {len(self.all_events)}")
        
        # ----------------------------------------
        # result save as csv
        # ----------------------------------------
        result_dir = "result"
        os.makedirs(result_dir, exist_ok=True)

        events_path = os.path.join(result_dir, "engine_events.csv")
        trades_path = os.path.join(result_dir, "engine_trades.csv")

        pd.DataFrame(self.all_events).to_csv(events_path, index=False)
        pd.DataFrame(self.all_trades).to_csv(trades_path, index=False)

        print(f"\nSaved events to: {events_path}")
        print(f"Saved trades to: {trades_path}")
        # ----------------------------------------

    def print_event(self, event):
        """
        Print event information and orderbook status for monitoring.
        """
        print(self.strategy)

        print(f"Timestamp : {event['timestamp']}")
        print(f"Signal    : {event['signal']}")
        print(f"Order ID  : {event['order_id']}")
        print(f"Trades    : {event['trades']}")
        print(f"All Trades: {self.all_trades}")  # Accumulated trades

        # Display OrderBook state
        order_book = self.gateway.order_book
        best_bid = order_book.best_bid()
        best_ask = order_book.best_ask()

        print("\n=== OrderBook State ===")

        # Best Bid
        if best_bid:
            print(
                f"Best Bid : {best_bid[0]}, "
                f"Order Price={-best_bid[0]}, "
                f"Order ID={best_bid[2].order_id}"
            )
        else:
            print("Best Bid : None")

        # Best Ask
        if best_ask:
            print(
                f"Best Ask : {best_ask[0]}, "
                f"Order Price={best_ask[0]}, "
                f"Order ID={best_ask[2].order_id}"
            )
        else:
            print("Best Ask : None")

        print("-" * 40)


# =============================
# run engine example
if __name__ == "__main__":
    # Change working directory to the project folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Load the intraday dataset
    df = pd.read_csv("data/AAPL_1m.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # Create Strategy + Gateway + Engine instances
    strategy = MACrossStrategy(short_window=10, long_window=20, position_size=1)
    gateway = Gateway()
    engine = Engine(gateway, strategy)

    # Run the simulation
    engine.run(df)
