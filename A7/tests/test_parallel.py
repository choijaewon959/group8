import pytest
import pandas as pd
import polars as pl
import numpy as np

from parallel import compute_metrics_threading, compute_metrics_multiprocessing

@pytest.fixture(scope="module")
def sample_data():
    np.random.seed(0)
    symbols = ["AAPL", "MSFT", "SPY"]
    n = 50
    timestamps = pd.date_range("2022-01-01", periods=n, freq="T")

    df = pd.DataFrame({
        "timestamp": np.tile(timestamps, len(symbols)),
        "symbol": np.repeat(symbols, n),
        "price": np.random.uniform(100, 200, n * len(symbols)),
    })
    df_polars = pl.from_pandas(df)
    return df, df_polars, symbols

def test_pandas_threading_multiprocessing(sample_data):
    df, _, symbols = sample_data

    res_thread = compute_metrics_threading(df, symbols, lib="pandas", window=5)
    res_multi = compute_metrics_multiprocessing(df, symbols, lib="pandas", window=5)

    # same symbols
    assert set(res_thread.keys()) == set(res_multi.keys())

    for sym in symbols:
        df_t = res_thread[sym]
        df_m = res_multi[sym]

        # same columns
        assert list(df_t.columns) == list(df_m.columns)
        # same # rows
        assert len(df_t) == len(df_m)

        # check mean price & mean Sharpe
        assert abs(df_t["price"].mean() - df_m["price"].mean()) < 1e-6
        sharpe_cols = [c for c in df_t.columns if "sharpe" in c]
        if sharpe_cols:
            diff = abs(df_t[sharpe_cols[0]].mean() - df_m[sharpe_cols[0]].mean())
            assert diff < 1e-5

def test_polars_threading_multiprocessing(sample_data):
    _, df_polars, symbols = sample_data

    res_thread = compute_metrics_threading(df_polars, symbols, lib="polars", window=5)
    res_multi = compute_metrics_multiprocessing(df_polars, symbols, lib="polars", window=5)

    assert set(res_thread.keys()) == set(res_multi.keys())

    for sym in symbols:
        df_t = res_thread[sym].to_pandas()
        df_m = res_multi[sym].to_pandas()

        assert list(df_t.columns) == list(df_m.columns)
        assert len(df_t) == len(df_m)
        assert abs(df_t["price"].mean() - df_m["price"].mean()) < 1e-5