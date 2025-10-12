import pytest
from data_loader import load_data
import datetime
from models import MarketDataPoint
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy,  NaiveMovingAverageStrategyOpti_memo, NaiveMovingAverageStrategyOpti_Numpy
from profiler import calculate_profile

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

def test_opti_strategy_runs_under_1sec():
    data_points = load_data()
    strategy_info = {'numpy': NaiveMovingAverageStrategyOpti_Numpy(),
                     'memoization': NaiveMovingAverageStrategyOpti_memo(),
                     'deque': WindowedMovingAverageStrategy()}

    #test if optimization with generator runs under 1sec
    opti_using_generator=strategy_info['generator']
    generator_profile = calculate_profile(opti_using_generator.generate_signals, data_points, tick_size=100000)
    assert generator_profile['timeit'] < 1
    assert generator_profile['memory_usage'] < 150

    # test if optimization with numpy runs under 1sec
    opti_using_numpy = strategy_info['numpy']
    numpy_profile = calculate_profile(opti_using_numpy.generate_signals, data_points, tick_size=100000)
    assert numpy_profile['timeit'] < 1
    assert numpy_profile['memory_usage'] < 250

    # test if optimization with memoization runs under 1sec
    opti_using_memo = strategy_info['memoization']
    memo_profile = calculate_profile(opti_using_memo.generate_signals, data_points, tick_size=100000)
    assert memo_profile['timeit'] < 1
    assert memo_profile['memory_usage'] < 250

    # test if optimization with deque runs under 1sec
    opti_using_deque = strategy_info['deque']
    deque_profile = calculate_profile(opti_using_deque.generate_signals, data_points, tick_size=100000)
    assert deque_profile['timeit'] < 1
    assert deque_profile['memory_usage'] < 250




