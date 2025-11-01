import time
import pandas as pd
import numpy as np
import polars as pl
from data_loader import load_data_pandas, load_data_polars
from metrics import rolling_metrics_pandas, rolling_metrics_polars
# for parallel programing library
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
# for measuring performance libraries
import psutil
from memory_profiler import memory_usage


def compute_metrics_threading(df, symbols, lib="pandas", window=20):
    # variables : df = loaded df / symbols = list of sybmol which is unique in df / lib = string pandas or polars / window = integer
    results = {}

    # context manager for each symbol's thread  
    with ThreadPoolExecutor(max_workers=len(symbols)) as executor:
        futures = {}
        # futures = {future obejct1 : 'AAPL', 
        #            future object2 : 'MSFT',
        #            future object3 : 'SPY' 
        #            } : key is a future object
        for s in symbols:
            # load on multi-thread process for each symbol 
            if lib == "pandas":
                futures[executor.submit(rolling_metrics_pandas, df, s, ["price"], window)] = s
            elif lib == "polars":
                futures[executor.submit(rolling_metrics_polars, df, s, ["price"], window)] = s
            else:
                raise ValueError(f"only pandas and polars are valid library")
        
        # use only key in dictionary:futures as an iterator
        # retrieve results from each thread
        for f in as_completed(futures):
            symbol = futures[f]
            result_df, elapsed = f.result()
            results[symbol] = (result_df, elapsed)
    
    return results


def compute_metrics_multiprocessing(df, symbols, lib="pandas", window=20):
    results = {}

    with ProcessPoolExecutor(max_workers=len(symbols)) as executor:
        futures = {}
        for s in symbols:
            if lib == "pandas":
                futures[executor.submit(rolling_metrics_pandas, df, s, ["price"], window)] = s
            elif lib == "polars":
                futures[executor.submit(rolling_metrics_polars, df, s, ["price"], window)] = s
            else:
                raise ValueError(f"only pandas and polars are valid library")

        for f in as_completed(futures):
            symbol = futures[f]
            result_df, elapsed = f.result()
            results[symbol] = (result_df, elapsed)
    
    return results



def measure_performance(func, *args, **kwargs):
    process = psutil.Process() 

    def wrapper():
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        return result, total_time

    mem_usage, (result, total_time) = memory_usage(wrapper, max_usage=True, retval=True)
    cpu_percent = process.cpu_percent(interval=None)

    return result, total_time, cpu_percent, mem_usage





if __name__ == "__main__":
    window = 30
    file_path = "./data/market_data-1.csv"

    df_pandas, _, _ = load_data_pandas(file_path)
    df_polars, _, _ = load_data_polars(file_path)
    # same csv data set. therefore set the only symbols list
    symbols = df_pandas['symbol'].unique().tolist()
    
    print("Threading Test (pandas)")
    threading_results, total_time, cpu, mem = measure_performance(compute_metrics_threading, df_pandas, symbols, "pandas", window)
    print(f"Threading - Time: {total_time:.2f}s, CPU: {cpu}%, Memory: {mem} MiB")

    print("Multiprocessing Test (pandas)")
    multiprocessing_results, total_time, cpu, mem = measure_performance(compute_metrics_multiprocessing, df_pandas, symbols, "pandas", window)
    print(f"Multiprocessing - Time: {total_time:.2f}s, CPU: {cpu}%, Memory: {mem} MiB")

    # Threading/Multiprocessing with Polars
    print("Threading Test (polars)")
    threading_results_polars, total_time, cpu, mem = measure_performance(compute_metrics_threading, df_polars, symbols, "polars", window)
    print(f"Threading (Polars) - Time: {total_time:.2f}s, CPU: {cpu}%, Memory: {mem} MiB")
    
    print("Multiprocessing Test (polars)")
    multiprocessing_results_polars, total_time, cpu, mem = measure_performance(compute_metrics_multiprocessing, df_polars, symbols, "polars", window)
    print(f"Multiprocessing (Polars) - Time: {total_time:.2f}s, CPU: {cpu}%, Memory: {mem} MiB")

