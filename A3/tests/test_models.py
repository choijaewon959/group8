import pytest
from src.data_loader import load_data
import datetime
from src.models import MarketDataPoint
from src.strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, MovingAverageStrategyMemo_Array, MovingAverageStrategyMemo_LRUCache
from src.profiler import calculate_profile

def test_strategies_correct():
    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price= 150.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
    ]

    input_sizes = [10, 10, 400]
    strategies_info = {'strategy': NaiveMovingAverageStrategy()}
    strategy = strategies_info['strategy']

    #window bigger than sample set
    signals0 = strategy.run(market_data, tick_size=input_sizes[0])
    assert signals0[0] == None
    signals1 = strategy.run(market_data, tick_size=input_sizes[1])
    assert signals1[0] == None


    #buy price on tick 2 > avg 2 prices so should yield a buy
    strategies_info_buy_window = {'strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_info_buy_window['strategy']
    signal2 = strategy.run(market_data, tick_size=input_sizes[0])
    assert signal2[1][1] == 1


    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=150.0),
    ]
    #sell price on tick 2 < avg 2 prices so should yield sell
    strategies_info_sell_window = {'strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_info_sell_window['strategy']
    signal3 = strategy.run(market_data, tick_size=input_sizes[0])
    assert signal3[1][1] == -1


    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=160.0),
    ]
    #avg price == price so should yield a hold signal
    strategies_info_hold_window = {'strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_info_hold_window['strategy']
    signal3 = strategy.run(market_data, tick_size=input_sizes[0])
    assert signal3[1][1] == 0


    market_data = [
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=150.0),
        MarketDataPoint(timestamp=datetime.datetime.now(), symbol='AAPL', price=150.0),
    ]
    #with same data both strategies should yield same result
    strategies_info_check = {'Strategy': {'Naive': NaiveMovingAverageStrategy(window=2),
                                   'Windowed': WindowedMovingAverageStrategy(window=2)}}
    naive = strategies_info_check['Strategy']['Naive']
    windowed = strategies_info_check['Strategy']['Windowed']

    signalNaive = naive.run(market_data, tick_size=input_sizes[0])
    signalWindowed = windowed.run(market_data, tick_size=input_sizes[0])
    assert signalNaive == signalWindowed

    #in case market data is unavailable
    strategies_check_edgecase = {'Strategy': NaiveMovingAverageStrategy(window=2)}
    strategy = strategies_check_edgecase['Strategy']
    signals = strategy.run([])
    assert signals == []

def test_opti_strategy_runs_under_1sec():
    data_points = load_data()
    strategy_info = {'memo_array': MovingAverageStrategyMemo_Array(),
                     'memo_lru_cache': MovingAverageStrategyMemo_LRUCache(),
                     'deque': WindowedMovingAverageStrategy()}
    
    # thresholds
    ONE_SECOND_MILLI = 1 * 1000 # milliseconds
    MEM_USAGE_MiB = 100 * 0.953674 # MiB

    # test if optimization with memo - array version runs under contraints
    opti_using_numpy = strategy_info['memo_array']
    numpy_profile = calculate_profile(opti_using_numpy.run, data_points, tick_size=100000)
    assert numpy_profile['timeit'] < ONE_SECOND_MILLI
    assert numpy_profile['memory_usage'] < MEM_USAGE_MiB

    # test if optimization with lru cache - array version runs under constraints
    opti_using_memo = strategy_info['memo_lru_cache']
    memo_profile = calculate_profile(opti_using_memo.run, data_points, tick_size=100000)
    assert memo_profile['timeit'] < ONE_SECOND_MILLI
    assert memo_profile['memory_usage'] < MEM_USAGE_MiB

    # test if optimization with deque runs under contraints
    opti_using_deque = strategy_info['deque']
    deque_profile = calculate_profile(opti_using_deque.run, data_points, tick_size=100000)
    assert deque_profile['timeit'] < ONE_SECOND_MILLI
    assert deque_profile['memory_usage'] < MEM_USAGE_MiB


def test_expected_hotspots():
    data_points = load_data()
    strategy_info = {'naive': NaiveMovingAverageStrategy(),
                     'memo_array': MovingAverageStrategyMemo_Array(),
                     'memo_lru_cache': MovingAverageStrategyMemo_LRUCache(),
                     'deque': WindowedMovingAverageStrategy()}

    #function that runs on every tick, expected to be hotspot for all strategies
    expected_hotspot = "generate_signals"

    non_opti_naive = strategy_info['naive']
    profile_naive = calculate_profile(non_opti_naive.run, data_points, tick_size=100000)
    top_funcs_naive = sorted(profile_naive['stats'], key=lambda x: x['cumulative_time'], reverse=True)[:5]
    top_funcs_naive = [f['function'] for f in top_funcs_naive]

    assert expected_hotspot in top_funcs_naive

    opti_using_memo_array = strategy_info['memo_array']
    profile_memo_array = calculate_profile(opti_using_memo_array.run, data_points, tick_size=100000)
    top_funcs_memo_array = sorted(profile_memo_array['stats'], key=lambda x: x['cumulative_time'], reverse=True)[:5]
    top_funcs_memo_array = [f['function'] for f in top_funcs_memo_array]

    assert expected_hotspot in top_funcs_memo_array

    opti_using_memo_lru_cache = strategy_info['memo_lru_cache']
    profile_memo_lru_cache = calculate_profile(opti_using_memo_lru_cache.run, data_points, tick_size=100000)
    top_funcs_memo_lru_cache = sorted(profile_memo_lru_cache['stats'], key=lambda x: x['cumulative_time'],
                                      reverse=True)[:5]
    top_funcs_memo_lru_cache = [f['function'] for f in top_funcs_memo_lru_cache]

    assert expected_hotspot in top_funcs_memo_lru_cache

    opti_using_deque = strategy_info['deque']
    profile_deque = calculate_profile(opti_using_deque.run, data_points, tick_size=100000)
    top_funcs_deque = sorted(profile_deque['stats'], key=lambda x: x['cumulative_time'],
                             reverse=True)[:5]
    top_funcs_deque = [f['function'] for f in top_funcs_deque]

    assert expected_hotspot in top_funcs_deque



