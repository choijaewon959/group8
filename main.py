import os
import json
from analytics import BetaDecorator, DrawdownDecorator, VolatilityDecorator
from data_loader import CSVAdapter
from patterns.factory_pattern import InstrumentFactory
from config.config import Config
from strategies import MeanReversionStrategy, BreakoutStrategy
from observers import SignalPublisher, LoggerObserver, AlertObserver
from commands import ExecuteOrderCommand, Broker, UndoOrderCommand
from invokers import Invoker



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
"""
decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(lambda: stock_prices)))
print(decorated())
"""
# Load market data using CSVAdapter
market_data = csv_adapter.get_market_data()
# print(market_data)




###-------------- Demonstrate trade lifecycle: signal → execution → undo → redo -------------------------
### Load strategy config
base_dir = os.path.dirname(__file__)
file_path = base_dir + "/config/strategy_params.json"
with open(file_path, "r") as f:
    config = json.load(f)

#Load publisher
publisher = SignalPublisher()

#Load observers
logger = LoggerObserver()
alert = AlertObserver()

#attach logger and alert
publisher.attach(logger)
publisher.attach(alert)

#import strategies
br = BreakoutStrategy(config["BreakoutStrategy"], publisher)
mr = MeanReversionStrategy(config["MeanReversionStrategy"], publisher)

#showcase interchangeability
for strategy in [br, mr]:
    print(f"Strategy: {strategy.__class__.__name__}")
    for tick in market_data:
        strategy.generate_signals(tick)


#import broker and invoker
broker = Broker()
invoker = Invoker()

#Instantiate a buy for 1 command
buy = ExecuteOrderCommand(broker, 1, "AAPL", 100, 150)
#Instantiate a sell for 1 command
sell = ExecuteOrderCommand(broker, -1, "AAPL", 100, 155)

#use invoker to execute 1 command buy
invoker.execute_command(buy)
#use invoker to execute 1 command sell
invoker.execute_command(sell)

#use invoker to undo & redo last commands
invoker.undo_last()
invoker.redo_last()