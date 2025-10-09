import timeit, cProfile, pstats, io
import contextlib
import matplotlib.pyplot as plt
from memory_profiler import memory_usage


def profile_function(func, *args, **kwargs):
    # Time profiling
    timeit_result = timeit.timeit(lambda: func(*args, **kwargs), number=1)
    print("="*40 + " TIMEIT RESULT " + "="*40)
    print(f"Execution time: {timeit_result:.6f} seconds")
    print("="*95)

    # cprofile profiling
    cProfile.runctx('func(*args, **kwargs)', globals(), locals(), 'restats')
    p = pstats.Stats('restats')
    print("="*40 + " CPROFILE RESULT " + "="*40)
    p.sort_stats('cumulative').print_stats(10)
    print("="*95)

    # memory profiling
    # buf = io.StringIO() 
    # with contextlib.redirect_stdout(buf):
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

def plot_profile_by_input(runtime, memory_usage, input_sizes):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # runtime plot
    axes[0].plot(input_sizes, runtime, marker='o')
    axes[0].set_title('Runtime Profiling')
    axes[0].set_xlabel('Input Size')
    axes[0].set_ylabel('Runtime (s)')
    axes[0].grid(True)

    # memory usage plot
    axes[1].plot(input_sizes, memory_usage, marker='o', color='orange')
    axes[1].set_title('Memory Usage Profiling')
    axes[1].set_xlabel('Input Size')
    axes[1].set_ylabel('Memory Usage (MiB)')
    axes[1].grid(True)  

    plt.tight_layout()
    plt.show()

