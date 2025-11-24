from config import *
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import CryptoDataStream
from strategy.ma_cross import MACrossStrategy
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.data.historical import CryptoHistoricalDataClient
from data_loader import *
from bar_builder import LiveBarBuilder
import ccxt.pro as ccxtpro 
import asyncio
import os

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# get data from alpaca
symbol = "BTC/USD"
# symbol = "AAPL"

# clients
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
stream = CryptoDataStream(API_KEY, SECRET_KEY)
# stream = StockDataStream(API_KEY, SECRET_KEY)

# strategy
strategy = MACrossStrategy()

# builder
bar_builder = LiveBarBuilder()


# callback function
async def handle_trade(data):
    print(f"TRADE: {data}")

    # depending on raw_data flag, this might be data.price or data.p
    price = getattr(data, "price", None) or getattr(data, "p", None)
    ts = getattr(data, "timestamp", None) or getattr(data, "t", None)

    if price is None or ts is None:
        return

    price = float(price)
    # Feed every trade into bar builder
    completed_bar = bar_builder.update(price=price, ts=ts)
    if completed_bar is None:
        return  # bar not completed yet

    row = {"close": completed_bar["close"]}
    strategy.update_live_bar(row, completed_bar["timestamp"])
    signal = strategy.generate_live_signal()

    if signal.action != "HOLD":
        print(f"Generated Signal: {signal}")

        side = OrderSide.BUY if signal.action == "BUY" else OrderSide.SELL

        # very dumb fixed size; change to your sizing logic
        order = MarketOrderRequest(
            symbol=symbol,
            qty=0.001,
            side=side,
            time_in_force=TimeInForce.GTC,
        )
        try:
            resp = trading_client.submit_order(order)
            print("Submitted order:", resp)
        except Exception as e:
            print("Order error:", e)


async def handle_quote(data):
    print(f"QUOTE: {data}")


# def main():
#     print(f"Subscribing to {symbol} trades and quotes...")

#     # subscribe async handlers
#     stream.subscribe_trades(handle_trade, symbol)
#     # stream.subscribe_quotes(handle_quote, symbol)

#     print("Starting crypto stream...")
#     stream.run()

# if __name__ == "__main__":
#     main()

async def main():
    # Public market data only
    exchange = ccxtpro.coinbaseexchange()  # Coinbase Exchange

    await exchange.load_markets()

    symbol = "BTC/USD"

    try:
        while True:
            # watch_trades returns most recent trades (streaming)
            trades = await exchange.watch_trades(symbol)
            for t in trades:
                print(
                    f"{symbol} {t['datetime']} "
                    f"price={t['price']} size={t['amount']} side={t['side']}"
                )
                p = t['price']
                ts = t['timestamp']

                if p is None or ts is None:
                    continue

                price = float(p)
                # Feed every trade into bar builder
                completed_bar = bar_builder.update(price=price, ts=ts)
                if completed_bar is None:
                    continue  # bar not completed yet

                row = {"close": completed_bar["close"]}
                strategy.update_live_bar(row, completed_bar["timestamp"])
                signal = strategy.generate_live_signal()
                
                if signal.action != "HOLD":
                    print(f"Generated Signal: {signal}")

                    side = OrderSide.BUY if signal.action == "BUY" else OrderSide.SELL

                    order = MarketOrderRequest(
                        symbol=symbol,
                        qty=0.001,
                        side=side,
                        time_in_force=TimeInForce.GTC,
                    )
                    try:
                        resp = trading_client.submit_order(order)
                        print("Submitted order:", resp)
                    except Exception as e:
                        print("Order error:", e)
    finally:            
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())





