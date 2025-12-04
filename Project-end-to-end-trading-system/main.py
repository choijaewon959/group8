from config import *
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import CryptoDataStream
from strategy.ma_cross import MACrossStrategy
from strategy.momentum import MomentumStrategy
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.data.historical import CryptoHistoricalDataClient
from data_loader import *
from bar_builder import LiveBarBuilder
from trade_logger import TradeLogger
import ccxt.pro as ccxtpro 
import asyncio
import os
import sys

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Initialize trade logger
trade_logger = TradeLogger()

# get data from alpaca
symbol = "BTC/USD"
# symbol = "AAPL"

# clients
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
stream = CryptoDataStream(API_KEY, SECRET_KEY)
# stream = StockDataStream(API_KEY, SECRET_KEY)

# strategy
strategy = MACrossStrategy(short_window=3, long_window=10, position_size=0.0001)
# strategy = MomentumStrategy(lookback=10, threshold=0.0001)

# builder
bar_builder = LiveBarBuilder(interval="1min")


def build_order(price, ts):
    if price is None or ts is None:
        return

    price = float(price)
    # Feed every trade into bar builder
    completed_bar = bar_builder.update(price=price, ts=ts)
    if completed_bar is None:
        return  # bar not completed yet

    print(f"Completed bar: {completed_bar}")
    
    row = {"close": completed_bar["close"]}
    strategy.update_live_bar(row, completed_bar["timestamp"])
    signal = strategy.generate_live_signal()

    print(f"Signal generated: {signal.action}, Qty: {signal.qty}")
    
    if signal.action != "HOLD":
        side = OrderSide.BUY if signal.action == "BUY" else OrderSide.SELL

        order = MarketOrderRequest(
            symbol=symbol,
            qty=signal.qty,
            side=side,
            time_in_force=TimeInForce.GTC,
        )
        try:
            resp = trading_client.submit_order(order)
            print("Submitted order:", resp)
            
            # Log successful order
            trade_logger.log_success(
                symbol=symbol,
                side=signal.action,
                qty=signal.qty,
                price=signal.price,
                strategy_name=signal.strategy_name,
                order_response=resp
            )
        except Exception as e:
            print("Order error:", e)
            
            # Log failed order
            trade_logger.log_failure(
                symbol=symbol,
                side=signal.action,
                qty=signal.qty,
                price=signal.price,
                strategy_name=signal.strategy_name,
                error=e
            )


# callback functions for alpaca streaming
async def handle_trade(data):
    print(f"TRADE: {data}")

    # depending on raw_data flag, this might be data.price or data.p
    price = getattr(data, "price", None) or getattr(data, "p", None)
    ts = getattr(data, "timestamp", None) or getattr(data, "t", None)
    build_order(price, ts)


async def handle_quote(data):
    print(f"QUOTE: {data}")


# main function for alpaca streaming
def main_al():
    print(f"Subscribing to {symbol} trades and quotes from Alpaca...")

    # subscribe async handlers
    stream.subscribe_trades(handle_trade, symbol)
    # stream.subscribe_quotes(handle_quote, symbol)

    print("Starting crypto stream...")
    stream.run()


# main function for coinbase streaming
async def main_cb():
    print(f"Subscribing to {symbol} trades and quotes from Coinbase ...")

    # Public market data only
    exchange = ccxtpro.coinbaseexchange()  # Coinbase Exchange

    await exchange.load_markets()
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
                build_order(p, ts)
    finally:            
        await exchange.close()

if __name__ == "__main__":
    print(f"Trade log initialized at {trade_logger.log_file}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "alpaca":
        main_al()
    else:
        asyncio.run(main_cb())





