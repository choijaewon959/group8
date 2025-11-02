import pytest
import pandas as pd
import polars as pl

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


