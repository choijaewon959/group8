import time
from data_loader import load_ticker_data, load_market_data
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import numpy as np
from sqlite_storage import retrieve_market_data

def csv_to_parquet(df: pd.DataFrame) -> pa.table:
    return pa.Table.from_pandas(df, preserve_index=False)

def partition_by_symbol(df: pa.Table):
     pq.write_to_dataset(
        df,
        root_path="output_parquet",
        partition_cols=["ticker"]     # partition by ticker symbol
    )

def load_parquet():
    dataset = ds.dataset("output_parquet",
                         format="parquet",
                         partitioning="hive"
                         )
    return dataset


def load_parquet_range(dataset, ticker, start, end):
    table = dataset.to_table(
        filter=(
            (ds.field("ticker") == ticker) &
            (ds.field("timestamp") >= start) &
            (ds.field("timestamp") <= end)
        )
    )

    return table.to_pandas()

def compute_rolling_vol(df):
    df = df.sort_values("timestamp")
    df["return"] = df["close"].pct_change()
    df["vol_5d"] = df["return"].rolling(5).std() * np.sqrt(252)
    return df

def compute_rolling_vol_per_symbol(dataset, tickers):
    df_vols = []
    for ticker in tickers:
        df = load_parquet_range(dataset, ticker, "2000-01-01", "2100-01-01")
        df_vol = compute_rolling_vol(df)
        df_vols.append(df_vol)

    return pd.concat(df_vols)


if __name__ == '__main__':
    tickers_table = load_ticker_data()
    tickers = tickers_table['symbol'].unique().tolist()
    market_data_table = load_market_data(tickers)

    print(f"Convert file to parquet...")
    market_data = csv_to_parquet(market_data_table)
    print(f"file in parquet format")

    print(f"Partition the file by ticker symbol...")
    partition_by_symbol(market_data)
    print(f"File partitioned")

    print(f"Load parquet dataset...")
    dataset = load_parquet()
    print("Done")

    print(f"retrieve all data for AAPL in 1 week...")
    dataset_AAPL = load_parquet_range(dataset, "AAPL", "2025-11-17", "2025-11-21")
    print("Done")

    print(f"Compute rolling 5-day volatility for each ticker...")
    rolling_vol = compute_rolling_vol_per_symbol(dataset, tickers)
    print("Done")

    print("assessing performance with parquet...")
    start = time.time()
    _ = load_parquet_range(dataset, "AAPL", "2025-11-17", "2025-11-21")
    end = time.time()
    print(f"parquet query time: {end-start}")

    print("assessing performance with sqlite...")
    db_path = 'market_data.db'
    start = time.time()
    _ = retrieve_market_data(db_path, 'AAPL', "2025-11-17", "2025-11-21")
    end = time.time()
    print(f"sqlite query time: {end-start}")











