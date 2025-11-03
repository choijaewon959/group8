import pytest
import pandas as pd
from patterns.builder_pattern import PortfolioBuilder
from portfolio import long_only_MA20_port_construction_with_time_series, compute_portfolio_metrics

@pytest.fixture
def mock_market_data():
    data = {
        "timestamp": pd.to_datetime([
            "2025-10-01 09:30"] * 60  # 20개씩 3종목
        ),
      # sample data from csv file
        "symbol": ["AAPL"] * 20 + ["MSFT"] * 20 + ["SPY"] * 20,
        "price": [
            169.89, 169.41, 169.73, 170.11, 170.24, 170.27, 170.05, 169.99, 170.00, 169.73,
            169.72, 170.04, 170.18, 169.74, 169.25, 169.25, 169.03, 169.34, 169.48, 169.85,
            320.22, 319.76, 319.54, 319.81, 320.29, 320.03, 320.15, 320.42, 320.75, 320.77,
            320.86, 320.62, 321.00, 321.41, 321.51, 321.90, 321.73, 322.21, 321.80, 322.22,
            430.06, 429.77, 429.97, 429.56, 429.56, 429.82, 429.40, 429.78, 429.52, 429.04,
            429.53, 430.01, 429.80, 429.79, 430.26, 429.84, 430.24, 430.50, 430.93, 430.96
        ]
    }
    return pd.DataFrame(data)

def test_portfolio_total_value(mock_market_data):
    main_builder = PortfolioBuilder("Main Portfolio", "wanann")
    sub_builder = PortfolioBuilder("SPY Portfolio", "wanann")

    long_only_MA20_port_construction_with_time_series(mock_market_data, "AAPL", main_builder)
    long_only_MA20_port_construction_with_time_series(mock_market_data, "SPY", sub_builder)

    main_builder.add_subportfolio(sub_builder.portfolio)

    try:
        final_metrics = compute_portfolio_metrics(main_builder.portfolio)
    except IndexError:
        final_metrics = {"total_value": 0.0}

    positions_total = sum(pos['quantity']*pos['price'] for pos in main_builder.portfolio.positions)
    sub_total = sum(pos['quantity']*pos['price'] for sub in main_builder.portfolio.sub_portfolios for pos in sub.positions)
    expected_total = positions_total + sub_total

    assert round(final_metrics["total_value"], 2) == round(expected_total, 2)
