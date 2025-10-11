from data_loader import load_data
from profiler import update_strategies_profile_info, plot_profile_by_input
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, NaiveMovingAverageStrategyOpti_memo, NaiveMovingAverageStrategyOpti_Numpy


def main():
    # 1. load data
    data_points = load_data() # tick data points

    # 2. initialize strategy
    input_sizes = [1000, 10_000, 100_000]
    strategies_info = {
        'naiveMA': {
            'strategy': NaiveMovingAverageStrategyOpti_Numpy(),
            'runtime_summary': [],
            'memory_summary': [],
            'input_sizes': input_sizes
        },
        'windowMA': {
            'strategy': WindowedMovingAverageStrategy(),
            'runtime_summary': [],
            'memory_summary': [],
            'input_sizes': input_sizes
        },
    }

    # 3. profile for each strategy
    update_strategies_profile_info(strategies_info, data_points)
    # # 4. output results
    plot_profile_by_input(strategies_info)


if __name__ == "__main__":
    main()