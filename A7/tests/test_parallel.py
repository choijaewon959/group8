from parallel import compute_metrics_threading, compute_metrics_multiprocessing

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