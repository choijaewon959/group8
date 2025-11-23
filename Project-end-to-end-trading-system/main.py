from config import *
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from strategy.ma_cross import MACrossStrategy
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.data.historical import CryptoHistoricalDataClient
from data_loader import *
import asyncio
import os

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# get data from alpaca
symbol = "BTC/USD"

# put into strategy
strategy = MACrossStrategy()
stream = StockDataStream(API_KEY, SECRET_KEY)

# callback function
async def handle_trade(data):
    print(f"TRADE: {data}")
    row = {
        "Close": data.price,
    }
    ts = data.timestamp
    strategy.update_live_bar(row, ts)
    signal = strategy.generate_live_signal()
    if signal.action != "HOLD":
        print(f"Generated Signal: {signal}")


async def handle_quote(data):
    print(f"QUOTE: {data}")


async def main():
    print(f"Subscribing to {symbol} trades and quotes...")
    stream.subscribe_trades(handle_trade, symbol)
    stream.subscribe_quotes(handle_quote, symbol)
    
    print("Starting stream...")
    await stream.run_fo()

        # Trading client (paper)
    trading_client = TradingClient(
        API_KEY,
        SECRET_KEY,
        paper=True    # <= VERY IMPORTANT
    )

    # Data client (crypto)
    data_client = CryptoHistoricalDataClient()


if __name__ == "__main__":
    asyncio.run(main())

# def run():
#     data = get_data_from_alpaca("AAPL", "2023-01-01", "2023-06-01", "1m")
    
#     strategy = MACrossStrategy()
#     for index, row in data.iterrows():
#         strategy.update_live_bar(row)
#         signal = strategy.generate_live_signal()
#         if signal.action != "HOLD":
#             print(f"Generated Signal: {signal}")


# if __name__ == "__main__":
#     run()

