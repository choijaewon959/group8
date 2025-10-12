import timeit, cProfile, pstats
from memory_profiler import memory_usage

def calculate_profile(func, *args, **kwargs):
    # Time profiling
    timeit_result = timeit.timeit(lambda: func(*args, **kwargs), number=1)
    timeit_result_millis = timeit_result * 1000  # Convert to milliseconds
    print("="*40 + " TIMEIT RESULT " + "="*40)
    print(f"Execution time: {timeit_result_millis:.3f} milliseconds")
    print("="*95)

    #cprofile profiling
    pr = cProfile.Profile()
    pr.enable()
    func(*args, **kwargs)
    pr.disable()
    
    stats = pstats.Stats(pr)
    parsed_stats = []
    for func_identifier, stat in stats.stats.items():
        filename, line, func_name = func_identifier
        ncalls, primitive, tottime, cumtime, callers = stat
        parsed_stats.append({
            "function": func_name,
            "file": filename,
            "line": line,
            "ncalls": ncalls,
            "primitive_calls": primitive,
            "total_time": tottime,
            "cumulative_time": cumtime
        })

    # memory profiling
    baseline_memory = memory_usage()[0]
    mem_usage = memory_usage((func, args, kwargs), interval=0.1)
    max_mem_usage = max(mem_usage)
    print("="*40 + " MEMORY PROFILER RESULT " + "="*40)
    print(f"Baseline memory: {baseline_memory:.2f} MiB")
    print(f"Peak memory usage: {max_mem_usage:.2f} MiB") 
    print(f"Strategy Peak memory usage: {max_mem_usage - baseline_memory:.2f} MiB") 
    print("="*95)

    return {
        'timeit': timeit_result_millis,
        'stats': parsed_stats,
        'memory_usage': max_mem_usage - baseline_memory
    }

def update_strategies_profile_info(strategies_info, data_points):
    for strategy_map in strategies_info.values():
        strategy = strategy_map['strategy']
        for tick_size in strategy_map['input_sizes']:
            profile = calculate_profile(strategy.run, data_points, tick_size=tick_size)
            strategy_map['runtime_summary'].append(profile['timeit'])
            strategy_map['memory_summary'].append(profile['memory_usage'])
            strategy_map['stats'].append(profile['stats'])

