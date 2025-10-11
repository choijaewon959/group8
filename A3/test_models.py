import pytest
import datetime
from models import MarketDataPoint
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy
from pathlib import Path
import csv

"""
FIXTURES = Path(__file__).parent
dUMMY_STRATEGY = "dummyStrategy"
BAD_STATUS = "BADSTATUS"
"""

def test_strategies_correct():
    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price= 150.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
    ]

    input_sizes = [10, 100, 400]
    strategies_info = {'strategy': NaiveMovingAverageStrategy()}
    strategy = strategies_info['strategy']

    #window bigger than sample set
    signals0 = strategy.generate_signals(market_data, tick_size=input_sizes[0])
    assert len(signals0) == 0
    signals1 = strategy.generate_signals(market_data, tick_size=input_sizes[1])
    assert len(signals1) == 0


    #buy price on tick 2 > avg 2 prices so should yield a buy
    strategies_info_buy_window = {'strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_info_buy_window['strategy']
    signal2 = strategy.generate_signals(market_data, tick_size=input_sizes[0])
    assert signal2[0][1] == "BUY"


    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=150.0),
    ]
    #sell price on tick 2 < avg 2 prices so should yield sell
    strategies_info_sell_window = {'strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_info_sell_window['strategy']
    signal3 = strategy.generate_signals(market_data, tick_size=input_sizes[0])
    assert signal3[0][1] == "SELL"


    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
    ]
    #avg price == price so should yield a hold signal
    strategies_info_hold_window = {'strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_info_hold_window['strategy']
    signal3 = strategy.generate_signals(market_data, tick_size=input_sizes[0])
    assert signal3[0][1] == "HOLD"


    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=150.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=150.0),
    ]
    #with same data both strategies should yield same result
    strategies_info_check = {'Strategy': {'Naive': NaiveMovingAverageStrategy(window=2),
                                   'Windowed': WindowedMovingAverageStrategy(window=2)}}
    naive = strategies_info_check['Strategy']['Naive']
    windowed = strategies_info_check['Strategy']['Windowed']

    signalNaive = naive.generate_signals(market_data, tick_size=input_sizes[0])
    signalWindowed = windowed.generate_signals(market_data, tick_size=input_sizes[0])
    assert signalNaive == signalWindowed

    #in case market data is unavailable
    strategies_check_edgecase = {'Strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_check_edgecase['Strategy']
    signals = strategy.generate_signals([])
    assert signals == []
