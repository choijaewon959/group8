from strategies import BreakoutStrategy, MeanReversionStrategy
from observers import SignalPublisher, LoggerObserver, AlertObserver
from models import MarketDataPoint

def test_length_of_return_data():
    market_data = MarketDataPoint("2025-10-25T12:00:00","AAPL", 185.23)

    strategy_params = {
            "lookback_window": 15,
            "threshold": 0.03
            }

    br = BreakoutStrategy(strategy_params, SignalPublisher())
    br_run = br.generate_signals(market_data)

    assert br_run == 0
