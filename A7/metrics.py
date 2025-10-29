import time
import pandas as pd
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from data_loader import load_data_pandas, load_data_polars


def rolling_metrics_pandas(df: pd.DataFrame, symbol: str, ts_cols: list, window=20) -> tuple[pd.DataFrame, float]:
    start = time.perf_counter()

    df_symbol = df[df["symbol"] == symbol].copy()
    df_symbol = df_symbol.sort_values("timestamp")

    for col in ts_cols:
        df_symbol[f"{col}_MA_{window}"] = (
            df_symbol[col].rolling(window=window).mean()
        )
        df_symbol[f"{col}_STD_{window}"] = (
            df_symbol[col].rolling(window=window).std(ddof=1)
        )

        df_symbol[f"{col}_rets"] = df_symbol[col].pct_change()
        df_symbol[f"{col}_rets_mean_{window}"] = (
            df_symbol[f"{col}_rets"].rolling(window=window).mean()
        )
        df_symbol[f"{col}_rets_std_{window}"] = (
            df_symbol[f"{col}_rets"].rolling(window=window).std(ddof=1)
        )
        df_symbol[f"{col}_sharpe_{window}"] = (
            df_symbol[f"{col}_rets_mean_{window}"] / df_symbol[f"{col}_rets_std_{window}"]
        )

        # annualize Sharpe ratio
        df_symbol[f"{col}_sharpe_{window}"] *= np.sqrt(252)

    end = time.perf_counter()
    elapsed_time = end - start

    return df_symbol, elapsed_time


def rolling_metrics_polars(df: pl.DataFrame, symbol: str, ts_cols: list, window: int = 20) -> tuple[pl.DataFrame, float]:
    start = time.perf_counter()

    df_symbol = df.filter(pl.col("symbol") == symbol).sort("timestamp")
    df_symbol = (
        df.filter(pl.col("symbol") == symbol)
            .sort("timestamp")
    )

    # Start with df_symbol so we can add multiple columns in one go
    for col in ts_cols:
        df_symbol = df_symbol.with_columns([
            # Rolling mean/std of price
            pl.col(col).rolling_mean(window_size=window).alias(f"{col}_MA_{window}"),
            pl.col(col).rolling_std(window_size=window, ddof=1).alias(f"{col}_STD_{window}"),

            # Returns
            pl.col(col).pct_change().alias(f"{col}_rets"),

            # Rolling mean/std on returns
            pl.col(col).pct_change().rolling_mean(window_size=window).alias(f"{col}_rets_mean_{window}"),
            pl.col(col).pct_change().rolling_std(window_size=window, ddof=1).alias(f"{col}_rets_std_{window}"),

            # Rolling Sharpe ratio (annualized)
            (
                pl.col(col).pct_change().rolling_mean(window_size=window) / pl.col(col).pct_change().rolling_std(window_size=window) * np.sqrt(252)
            ).alias(f"{col}_sharpe_{window}")
        ])

    end = time.perf_counter()
    elapsed_time = end - start

    return df_symbol, elapsed_time


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
    df_pandas_metrics, elapsed_time = rolling_metrics_pandas(df_pandas, symbol, ['price'], window=window)
    plot_rolling_metrics(df_pandas_metrics, window=window, subsample_size=subsample_size)

    df_polars, _, _ = load_data_polars(file_path)
    df_polars_metrics, elapsed_time = rolling_metrics_polars(df_polars, symbol, ['price'], window=window)
    plot_rolling_metrics(df_polars_metrics, window=window, subsample_size=subsample_size)
