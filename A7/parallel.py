import time
import psutil
import pandas as pd
import polars as pl
from data_loader import load_data_pandas, load_data_polars
from metrics import compute_rolling_metrics_pandas, compute_rolling_metrics_polars
from memory_profiler import memory_usage
from concurrent.futures import ThreadPoolExecutor, as_completed

def rolling_metrics_pandas_parallel(df: pd.DataFrame, ts_cols: list, window: int = 20, max_workers: int = 4):
    symbols = df["symbol"].unique()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(
                compute_rolling_metrics_pandas,
                df,
                symbol,
                ts_cols,
                window
            ): symbol for symbol in symbols
        }

        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                result_df, _ = future.result()
                results.append(result_df)
                print(f"Completed {symbol}...!")
            except Exception as e:
                print(f"Error computing {symbol}: {e}...!")

    return pd.concat(results, ignore_index=True)


def rolling_metrics_polars_parallel(df: pl.DataFrame, ts_cols: list, window: int = 20, max_workers: int = 4):
    symbols = df["symbol"].unique().to_list()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(
                compute_rolling_metrics_polars,
                df,
                symbol,
                ts_cols,
                window
            ): symbol for symbol in symbols
        }

        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                result_df, _ = future.result()
                results.append(result_df)
                print(f"Completed {symbol}...!")
            except Exception as e:
                print(f"Error computing {symbol}: {e}...!")

    return pl.concat(results)



if __name__ == "__main__":
    symbol = 'AAPL'
    window = 20
    subsample_size = 1000
    file_path = "./data/market_data-1.csv"

    df_pandas, _, _ = load_data_pandas(file_path)
    df_result_pd = rolling_metrics_pandas_parallel(df_pandas, ["price"], window=20, max_workers=4)
    print(df_result_pd.tail())

    df_polars, _, _ = load_data_polars(file_path)
    df_result_pl = rolling_metrics_polars_parallel(df_polars, ["price"], window=20, max_workers=4)
    print(df_result_pl.tail())
