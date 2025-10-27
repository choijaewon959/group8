from strategies import BreakoutStrategy, MeanReversionStrategy
from observers import SignalPublisher, LoggerObserver, AlertObserver
from models import MarketDataPoint

def test_length_of_return_data():
    strategy_params = {
        "lookback_window": 15,
        "threshold": 0.03
    }

    market_data = MarketDataPoint("2025-10-25T12:00:00","AAPL", 185.23)
    br = BreakoutStrategy(strategy_params, SignalPublisher())
    br_run = br.generate_signals(market_data)
    assert br_run == 0

    market_data = []
    br = BreakoutStrategy(strategy_params, SignalPublisher())
    br_run = br.generate_signals(market_data)
    assert br_run == 0


def test_mean_reversion_going_long():
    class mockPublisher():
        def __init__(self):
            self.trades = []

        def notify(self, signal):
            self.trades.append(signal)

    publisher = mockPublisher()
    strategy_params = {
                "lookback_window": 2,
                "threshold": 0.02
                }

    strategy = MeanReversionStrategy(strategy_params, publisher)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 185.23)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120)
    signal = strategy.generate_signals(market_data)

    #should have a buy signal when price is below mean
    assert signal["signal"] == 1
    #Only 1 buy signal so observers should only be notified once
    assert len(publisher.trades) == 1
    assert publisher.trades[0]["strategy"] == "MeanReversionStrategy"


def test_mean_reversion_going_short():
    class mockPublisher():
        def __init__(self):
            self.trades = []

        def notify(self, signal):
            self.trades.append(signal)

    publisher = mockPublisher()
    strategy_params = {
                "lookback_window": 2,
                "threshold": 0.02
                }

    strategy = MeanReversionStrategy(strategy_params, publisher)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 180)
    signal = strategy.generate_signals(market_data)

    #should have a sell signal when price is above mean
    assert signal["signal"] == -1
    #Only 1 sell signal so observers should only be notified once
    assert len(publisher.trades) == 1
    assert publisher.trades[0]["strategy"] == "MeanReversionStrategy"


def test_mean_reversion_no_signal():
    class mockPublisher():
        def __init__(self):
            self.trades = []

        def notify(self, signal):
            self.trades.append(signal)

    publisher = mockPublisher()
    strategy_params = {
                "lookback_window": 2,
                "threshold": 0.02
                }

    strategy = MeanReversionStrategy(strategy_params, publisher)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 121)
    signal = strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120.5)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120.2)
    signal = strategy.generate_signals(market_data)

    assert publisher.trades == []



def test_breakout_strategy_going_short():
    class mockPublisher():
        def __init__(self):
            self.trades = []

        def notify(self, signal):
            self.trades.append(signal)

    publisher = mockPublisher()
    strategy_params = {
                "lookback_window": 1,
                "threshold": 0.02
                }

    strategy = BreakoutStrategy(strategy_params, publisher)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 185.23)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120)
    signal = strategy.generate_signals(market_data)

    #should have a buy signal when price is below mean
    assert signal["signal"] == -1
    #Only 1 buy signal so observers should only be notified once
    assert len(publisher.trades) == 1
    assert publisher.trades[0]["strategy"] == "BreakoutStrategy"


def test_Breakout_Strategy_going_long():
    class mockPublisher():
        def __init__(self):
            self.trades = []

        def notify(self, signal):
            self.trades.append(signal)

    publisher = mockPublisher()
    strategy_params = {
                "lookback_window": 1,
                "threshold": 0.02
                }

    strategy =  BreakoutStrategy(strategy_params, publisher)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 180)
    signal = strategy.generate_signals(market_data)

    #should have a sell signal when price is above mean
    assert signal["signal"] == 1
    #Only 1 sell signal so observers should only be notified once
    assert len(publisher.trades) == 1
    assert publisher.trades[0]["strategy"] == "BreakoutStrategy"


def test_Breakout_Strategy_no_signal():
    class mockPublisher():
        def __init__(self):
            self.trades = []

        def notify(self, signal):
            self.trades.append(signal)

    publisher = mockPublisher()
    strategy_params = {
                "lookback_window": 1,
                "threshold": 0.02
                }

    strategy = BreakoutStrategy(strategy_params, publisher)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 121)
    signal = strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120.5)
    strategy.generate_signals(market_data)
    market_data = MarketDataPoint("2025-10-25T12:00:00", "AAPL", 120.2)
    signal = strategy.generate_signals(market_data)

    assert publisher.trades == []