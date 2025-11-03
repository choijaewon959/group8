import pytest
import pandas as pd
import polars as pl
import numpy as np

@pytest.fixture
def mock_market_data():
    """Fixture to provide sample data for testing pandas."""
    data = {
        "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="D"),
        "symbol": ["AAPL"] * 100,
        "price": [i for i in range(1, 101)]
    }
    return { 
        'pandas' :pd.DataFrame(data),
        'polars': pl.DataFrame(data)
    }

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

