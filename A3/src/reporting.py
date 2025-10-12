import pandas as pd
import os
import matplotlib.pyplot as plt

def get_result_dir():
    result_dir = os.path.join(os.path.dirname(__file__), '../', 'result')
    os.makedirs(result_dir, exist_ok=True)

    return result_dir

def plot_profile_by_input(strategies):
    _, axes = plt.subplots(1, 2, figsize=(12, 5))

    for strategy_name, strategy_info in strategies.items():
        runtime = strategy_info['runtime_summary']
        memory_usage = strategy_info['memory_summary']
        input_sizes = strategy_info['input_sizes']

        # Runtime subplot
        axes[0].plot(input_sizes, runtime, marker='o', label=strategy_name)
        for x, y in zip(input_sizes, runtime):
            axes[0].text(x, y, f"{y:.2f}", fontsize=8, ha='right', va='bottom')

        # Memory subplot
        axes[1].plot(input_sizes, memory_usage, marker='o', label=strategy_name)
        for x, y in zip(input_sizes, memory_usage):
            axes[1].text(x, y, f"{y:.2f}", fontsize=8, ha='right', va='bottom')

    # Titles and labels
    axes[0].set_title('Runtime Profiling')
    axes[0].set_xlabel('Input Size')
    axes[0].set_ylabel('Runtime (ms)')
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
    plt.savefig(os.path.join(get_result_dir(), "profiling_results.png"))

    plt.show()

def print_out_result(strategies):
    for strategy_name, strategy_info in strategies.items():
        print(f"Strategy: {strategy_name}")
        print(f"  Input Sizes: {strategy_info['input_sizes']}")
        print(f"  Runtime Summary: {strategy_info['runtime_summary']}")
        print(f"  Memory Summary: {strategy_info['memory_summary']}")
        
        runtime_stat = []
        for input_size, info in zip(strategy_info['input_sizes'], strategy_info['stats']):
            for log in info:
                log['input_size'] = input_size
                runtime_stat.append(log)
        df = pd.DataFrame(runtime_stat)
        df.to_csv(os.path.join(get_result_dir(), f"runtime_stat_{strategy_name}.csv"), index=False)

    
