import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from gateway import Gateway
from strategy.ma_cross import MACrossStrategy

# csv
df = pd.read_csv("data/AAPL_1m.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")

# Gateway + Strategy
gw = Gateway()
strategy = MACrossStrategy(short_window=10, long_window=20, position_size=1)

# streaming
print("=== CSV → Gateway Stream Test ===\n")

for event in gw.stream_data(df, strategy):
    print(strategy)
    print(f"Timestamp : {event['timestamp']}")
    print(f"Signal    : {event['signal']}")
    print(f"Order ID  : {event['order_id']}")
    print(f"Trades    : {event['trades']}")
    print("-" * 40)

print("\n=== TEST COMPLETE ===")
