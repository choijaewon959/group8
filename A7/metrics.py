import pandas as pd
import numpy as np
import polars as pl
from data_loader import load_data_pandas, load_data_polars
from reporting import plot_rolling_metrics


def rolling_metrics_pandas(df: pd.DataFrame, symbol: str, ts_cols: list, window=20) -> tuple[pd.DataFrame, float]:
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

    return df_symbol


def rolling_metrics_polars(df: pl.DataFrame, symbol: str, ts_cols: list, window: int = 20) -> tuple[pl.DataFrame, float]:
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

    return df_symbol



if __name__ == "__main__":
    symbol = 'AAPL'
    window = 20
    subsample_size = 1000
    file_path = "./data/market_data-1.csv"

    df_pandas, _, _ = load_data_pandas(file_path)
    df_pandas_metrics = rolling_metrics_pandas(df_pandas, symbol, ['price'], window=window)
    plot_rolling_metrics(df_pandas_metrics, window=window, subsample_size=subsample_size)

    df_polars, _, _ = load_data_polars(file_path)
    df_polars_metrics = rolling_metrics_polars(df_polars, symbol, ['price'], window=window)
    plot_rolling_metrics(df_polars_metrics, window=window, subsample_size=subsample_size)
