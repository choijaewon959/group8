import pandas as pd
import polars as pl


def load_data_pandas(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, parse_dates=True).set_index('timestamp', drop=False)
    return df

def load_data_polars(file_path: str) -> pl.DataFrame:
    df = (
        pl.read_csv(file_path, has_header=True, try_parse_dates=True)
          .sort("timestamp")
          .with_columns(pl.col("timestamp").alias("_index"))
    )
    return df

if __name__ == "__main__":
    pandas_df = load_data_pandas("./data/market_data-1.csv")
    print("Pandas DataFrame:")
    print(pandas_df.head())

    polars_df = load_data_polars("./data/market_data-1.csv")
    print("\nPolars DataFrame:")
    print(polars_df.head())