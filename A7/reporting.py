import time
import threading
import psutil
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
from data_loader import load_data_pandas, load_data_polars
from metrics import compute_rolling_metrics_pandas, compute_rolling_metrics_polars


def profiled_task(func, df, symbol, ts_cols, window):
    process = psutil.Process()
    start_time = time.time()
    start_cpu_times = process.cpu_times()
    start_mem = process.memory_info().rss / (1024 ** 2)

    # Run the actual computation
    result_df = func(df, symbol, ts_cols, window)

    end_time = time.time()
    end_cpu_times = process.cpu_times()
    end_mem = process.memory_info().rss / (1024 ** 2)

    metrics = {
        "symbol": symbol,
        "thread_id": threading.get_ident(),
        "elapsed_time_s": end_time - start_time,
        "cpu_user_s": end_cpu_times.user - start_cpu_times.user,
        "cpu_system_s": end_cpu_times.system - start_cpu_times.system,
        "mem_used_MB": end_mem - start_mem,
    }

    return symbol, result_df, metrics


def plot_rolling_metrics(df: pd.DataFrame, window: int = 20, subsample_size: int = 5000):
    # Convert Polars DataFrame to Pandas if necessary
    if isinstance(df, pl.DataFrame):
        df = df.to_pandas()

    # Ensure timestamp is the index
    if "timestamp" in df.columns:
        df = df.sort_values("timestamp").set_index("timestamp")

    df = df[window:subsample_size].copy()

    _, axes = plt.subplots(3, 1, figsize=(10,8), sharex=True)

    # Price & MA
    axes[0].plot(df.index, df["price"], color="tab:blue", label="Price")
    axes[0].plot(df.index, df[f"price_MA_{window}"], "--", color="tab:cyan", label=f"{window}-Day MA")
    axes[0].set_ylabel("Price")
    axes[0].legend(loc="upper left")

    # Volatility
    axes[1].plot(df.index, df[f"price_STD_{window}"], color="tab:orange", label="Volatility")
    axes[1].set_ylabel("Volatility")
    axes[1].legend(loc="upper left")

    # Sharpe
    axes[2].plot(df.index, df[f"price_sharpe_{window}"], color="tab:red", label="Sharpe Ratio")
    axes[2].set_ylabel("Sharpe (Annualized)")
    axes[2].legend(loc="upper left")

    plt.suptitle("Rolling Metrics Over Time")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    symbol = 'AAPL'
    window = 20
    subsample_size = 1000
    file_path = "./data/market_data-1.csv"

    df_pandas, _, _ = load_data_pandas(file_path)
    df_pandas_metrics, elapsed_time = compute_rolling_metrics_pandas(df_pandas, symbol, ['price'], window=window)
    print(f"Pandas elapsed time: {elapsed_time:.2f} seconds")
    plot_rolling_metrics(df_pandas_metrics, window=window, subsample_size=subsample_size)

    df_polars, _, _ = load_data_polars(file_path)
    df_polars_metrics, elapsed_time = compute_rolling_metrics_polars(df_polars, symbol, ['price'], window=window)
    print(f"Polars elapsed time: {elapsed_time:.2f} seconds")
    plot_rolling_metrics(df_polars_metrics, window=window, subsample_size=subsample_size)
