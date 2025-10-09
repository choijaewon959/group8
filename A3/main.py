


from data_loader import load_data
from profiler import profile_function, plot_profile_by_input


def main():
    # 1. load data
    data_points = load_data() # tick data points

    # 2. initialize strategy

    # 3. profile strategy
    def sort(data):
        data.sort(key=lambda x: x.price)

    profile = profile_function(sort, data_points)

    # 4. output results
    plot_profile_by_input(
        runtime=[profile['timeit']],
        memory_usage=[profile['memory_usage']],
        input_sizes=[len(data_points)]
    )


if __name__ == "__main__":
    main()