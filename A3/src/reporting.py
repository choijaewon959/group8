import matplotlib.pyplot as plt

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
    
