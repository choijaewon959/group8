from data_loader import load_data
from profiler import update_strategies_profile_info
from reporting import plot_profile_by_input, print_out_result
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy, MovingAverageStrategyMemo_LRUCache, MovingAverageStrategyMemo_Array


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
        'MAOptimized_memo_LRU_Cache': {
            'strategy': MovingAverageStrategyMemo_LRUCache(),
            'runtime_summary': [],
            'memory_summary': [],
            'stats': [],
            'input_sizes': input_sizes
        },
        'MAOptimized_memo_Array': {
            'strategy': MovingAverageStrategyMemo_Array(),
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
        
    }

    # 3. profile for each strategy
    update_strategies_profile_info(strategies_info, data_points)
    # 4. print out results
    print_out_result(strategies_info)
    # 5. output results
    plot_profile_by_input(strategies_info)


if __name__ == "__main__":
    main()