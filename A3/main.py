from data_loader import load_data
from profiler import update_strategies_profile_info, plot_profile_by_input
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy,MovingAverageStrategyMemo_Array, MovingAverageStrategyMemo_LRUCache,NaiveMovingAverageStrategyOpti_Numpy


def main():
    # 1. load data
    data_points = load_data() # tick data points

    # 2. initialize strategy
    input_sizes = [1000, 10_000, 100_000]
    strategies_info = {
        'naiveMA': {
            'strategy': NaiveMovingAverageStrategy(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'windowMA': {
            'strategy': WindowedMovingAverageStrategy(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'naiveMAOptimized_memo': {
            'strategy': NaiveMovingAverageStrategyOpti_memo(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'naiveMAOptimized_memo2': {
            'strategy': NaiveMovingAverageStrategyOptiMemo2(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'naiveMAOptimized_memo3': {
            'strategy': NaiveMovingAverageStrategyOptiMemo3(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'naiveMAOptimized_numpy': {
            'strategy': NaiveMovingAverageStrategyOpti_Numpy(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'naiveMAOptimized_generator': {
            'strategy': NaiveMovingAverageStrategyOpti_generator(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },  
        

    }

    # 3. profile for each strategy
    update_strategies_profile_info(strategies_info, data_points)
    # # 4. output results
    plot_profile_by_input(strategies_info)


if __name__ == "__main__":
    main()