from config import *
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from strategy.ma_cross import MACrossStrategy
from alpaca.data.live import StockDataStream
from data_loader import *
import asyncio
import os

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# get data from alpaca
symbol = "AAPL"

# put into strategy
strategy = MACrossStrategy()
stream = StockDataStream(API_KEY, SECRET_KEY)

# callback function
async def handle_trade(data):
    print(data)
    row = {
        "Close": data.price,
    }
    ts = data.timestamp
    strategy.update_live_bar(row, ts)
    signal = strategy.generate_live_signal()
    if signal.action != "HOLD":
        print(f"Generated Signal: {signal}")


async def handle_quote(data):
    print("QUOTE:", data)


async def main():
    stream.subscribe_trades(handle_trade, "AAPL")
    stream.subscribe_quotes(handle_quote, "AAPL")

    await stream._run_forever()


if __name__ == "__main__":
    asyncio.run(main())




