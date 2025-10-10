from itertools import product
from data_loader import load_data
from profiler import profile_function, plot_profile_by_input
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy


def main():
    # 1. load data
    data_points = load_data() # tick data points

    # 2. initialize strategy
    strategies_info = {
        'naiveMA': {
            'strategy': NaiveMovingAverageStrategy(),
            'runtime_summary': [],
            'memory_summary': [],
            'input_sizes': [10, 100, 400]
        },
        'windowMA': {
            'strategy': WindowedMovingAverageStrategy(),
            'runtime_summary': [],
            'memory_summary': [],
            'input_sizes': [10, 100, 400]
        },
    }

    # 3. profile for each strategy
    for strategy_map in strategies_info.values():
        strategy = strategy_map['strategy']
        for tick_size in strategy_map['input_sizes']:
            profile = profile_function(strategy.generate_signals, data_points, tick_size=tick_size)
            strategy_map['runtime_summary'].append(profile['timeit'])
            strategy_map['memory_summary'].append(profile['memory_usage'])

    # # 4. output results
    plot_profile_by_input(strategies_info)


if __name__ == "__main__":
    main()