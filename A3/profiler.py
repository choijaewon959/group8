import timeit, cProfile, pstats, io
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

def profile_function(func, *args, **kwargs):
    # Time profiling
    timeit_result = timeit.timeit(lambda: func(*args, **kwargs), number=1)
    print("="*40 + " TIMEIT RESULT " + "="*40)
    print(f"Execution time: {timeit_result:.6f} seconds")
    print("="*95)

    #cprofile profiling
    pr = cProfile.Profile()
    pr.enable()
    func(*args, **kwargs)
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)

    # memory profiling
    mem_usage = memory_usage((func, args, kwargs), interval=0.1)
    max_mem_usage = max(mem_usage)
    print("="*40 + " MEMORY PROFILER RESULT " + "="*40)
    print(f"Peak memory usage: {max_mem_usage:.2f} MiB")    
    print("="*95)

    return {
        'timeit': timeit_result,
        # 'cprofile': p,
        'memory_usage': max_mem_usage
    }

def update_strategies_profile_info(strategies_info, data_points):
    for strategy_map in strategies_info.values():
        strategy = strategy_map['strategy']
        for tick_size in strategy_map['input_sizes']:
            profile = profile_function(strategy.generate_signals, data_points, tick_size=tick_size)
            strategy_map['runtime_summary'].append(profile['timeit'])
            strategy_map['memory_summary'].append(profile['memory_usage'])

def plot_profile_by_input(strategies):
    _, axes = plt.subplots(1, 2, figsize=(12, 5))

    for strategy_name, strategy_info in strategies.items():
        runtime = strategy_info['runtime_summary']
        memory_usage = strategy_info['memory_summary']
        input_sizes = strategy_info['input_sizes']

        # Runtime subplot
        axes[0].plot(input_sizes, runtime, marker='o', label=strategy_name)
        # Memory subplot
        axes[1].plot(input_sizes, memory_usage, marker='o', label=strategy_name)

    # Titles and labels
    axes[0].set_title('Runtime Profiling')
    axes[0].set_xlabel('Input Size')
    axes[0].set_ylabel('Runtime (s)')
    axes[0].grid(True)

    axes[1].set_title('Memory Usage Profiling')
    axes[1].set_xlabel('Input Size')
    axes[1].set_ylabel('Memory Usage (MiB)')
    axes[1].grid(True)

    # Shared legend
    axes[0].legend()
    axes[1].legend()

    # Overall title
    plt.suptitle("Profiling Results for All Strategies", fontsize=14)
    plt.tight_layout()
    plt.show()
    

