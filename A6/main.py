import os
import json
from analytics import BetaDecorator, DrawdownDecorator, VolatilityDecorator
from data_loader import CSVAdapter
from patterns.factory_pattern import InstrumentFactory
from config.config import Config

SYMBOLS = ["AAPL", "MSFT", "US10Y", "SPY"]

# Load configuration
config = Config()
# base_dir = os.path.dirname(__file__)
# file_path = base_dir + "/config/config.json"
# with open(file_path, "r") as f:
#     config = json.load(f)

# Load toy data using CSVAdapter
csv_adapter = CSVAdapter()
raw_instruments = []
for symbol in SYMBOLS:
    data = csv_adapter.get_data(symbol)
    raw_instruments.extend(data)

symbol_map = {}
for d in raw_instruments:
    obj = InstrumentFactory.create_instrument(d)
    symbol_map[d["symbol"]] = obj

AAPL_stock = symbol_map.get("AAPL")
MSFT_stock = symbol_map.get("MSFT")
US10Y_bond = symbol_map.get("US10Y")
SPY_etf = symbol_map.get("SPY")

stock_prices = [AAPL_stock.price, MSFT_stock.price]

decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(lambda: stock_prices)))
print(decorated())

# Load market data using CSVAdapter
market_data = csv_adapter.get_market_data()
# print(market_data)


"""
from commands import ExecuteOrderCommand, Broker
from invokers import Invoker

broker = Broker()
invoker = Invoker

buy = ExecuteOrderCommand(broker, 1, "AAPL", 100, 150)
sell = ExecuteOrderCommand(broker, -1, "AAPL", 100, 155)

invoker.execute_command(buy)
invoker.execute_command(sell)

invoker.undo_last()

invoker.redo_last()

"""
