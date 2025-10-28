import time
import pandas as pd
import polars as pl
from memory_profiler import memory_usage

def load_data_pandas(file_path: str) -> pd.DataFrame:
    start = time.perf_counter()
    df = pd.read_csv(file_path, parse_dates=True).set_index('timestamp', drop=False)
    end = time.perf_counter()

    elapsed_time = end - start
    mem = memory_usage((pd.read_csv, (file_path,)), max_usage=True)    
    return df, elapsed_time, mem

def load_data_polars(file_path: str) -> pl.DataFrame:
    start = time.perf_counter()
    df = (
        pl.read_csv(file_path, has_header=True, try_parse_dates=True)
          .sort("timestamp")
          .with_columns(pl.col("timestamp").alias("_index"))
    )
    end = time.perf_counter()

    elapsed_time = end - start
    mem = memory_usage((pl.read_csv, (file_path,)), max_usage=True)

    return df, elapsed_time, mem

if __name__ == "__main__":
    pandas_df, pandas_time, pandas_mem = load_data_pandas("./data/market_data-1.csv")
    print("Pandas DataFrame:")
    print(pandas_df.head())
    print(f"Elapsed Time: {pandas_time:.4f} seconds")
    print(f"Memory Usage: {pandas_mem} MiB")

    polars_df, polars_time, polars_mem = load_data_polars("./data/market_data-1.csv")
    print("\nPolars DataFrame:")
    print(polars_df.head())
    print(f"Elapsed Time: {polars_time:.4f} seconds")
    print(f"Memory Usage: {polars_mem} MiB")