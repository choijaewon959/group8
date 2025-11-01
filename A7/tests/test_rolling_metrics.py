import numpy as np
from metrics import rolling_metrics_pandas, rolling_metrics_polars


def test_compute_rolling_metrics_pandas(mock_market_data):
    df_metrics = rolling_metrics_pandas(mock_market_data['pandas'], "AAPL", ['price'], window=20)

    assert not df_metrics['price_MA_20'].isnull().all()
    assert not df_metrics['price_STD_20'].isnull().all()
    assert not df_metrics['price_sharpe_20'].isnull().all()
    assert df_metrics['price_MA_20'].iloc[-1] == 90.5
    assert round(df_metrics['price_STD_20'].iloc[-1], 2) == 5.92
    assert round(df_metrics['price_sharpe_20'].iloc[-1], 2) == 238.96


def test_compute_rolling_metrics_polars(mock_market_data):
    df_metrics = rolling_metrics_polars(mock_market_data['polars'], "AAPL", ['price'], window=20)

    assert not df_metrics['price_MA_20'].is_null().all()
    assert not df_metrics['price_STD_20'].is_null().all()
    assert not df_metrics['price_sharpe_20'].is_null().all()
    assert df_metrics['price_MA_20'][-1] == 90.5
    assert round(df_metrics['price_STD_20'][-1], 2) == 5.92
    assert round(df_metrics['price_sharpe_20'][-1], 2) == 238.96


def test_pandas_polars_equivalence(mock_market_data):
    df_metrics_pd = rolling_metrics_pandas(mock_market_data['pandas'], "AAPL", ['price'], window=20)
    df_metrics_pl = rolling_metrics_polars(mock_market_data['polars'], "AAPL", ['price'], window=20)

    # ensure results are the same for any random index
    test_index = np.random.randint(30, 101)
    assert(round(df_metrics_pd['price_MA_20'].iloc[test_index], 2) == round(df_metrics_pl['price_MA_20'][test_index], 2))
    assert(round(df_metrics_pd['price_STD_20'].iloc[test_index], 2) == round(df_metrics_pl['price_STD_20'][test_index], 2))
    assert(round(df_metrics_pd['price_sharpe_20'].iloc[test_index], 2) == round(df_metrics_pl['price_sharpe_20'][test_index], 2))