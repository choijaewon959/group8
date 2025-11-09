import numpy as np
from strategy import SimplePriceStrategy, NewsSentimentStrategy

# Mock shared memory replacements
class MockPriceBook:
    def __init__(self, prices):
        self.prices = prices
        self.index = 0

    def read(self, symbol):
        price = self.prices[self.index]
        self.index = min(self.index + 1, len(self.prices)-1)
        return price


class MockNewsBook:
    def __init__(self, sentiments):
        self.sentiments = sentiments
        self.index = 0

    def read(self, symbol):
        sentiment = self.sentiments[self.index]
        self.index = min(self.index + 1, len(self.sentiments)-1)
        return sentiment


def test_price_strategy_buy_signal():
    # for normal case
    prices = [100, 101, 102, 103, 190]  
    mock_book = MockPriceBook(prices)
    strat = SimplePriceStrategy("AAPL", mock_book, window=3)

    # feed enough prices
    for _ in prices:
        signal = strat.generate_signal()

    assert signal is not None
    assert signal["signal"] == "BUY"
    assert signal["symbol"] == "AAPL"


def test_price_strategy_no_signal_until_window_full():

    prices = [100, 101]  # less than window size 
    mock_book = MockPriceBook(prices)
    strat = SimplePriceStrategy("AAPL", mock_book, window=3)

    for _ in prices:
        signal = strat.generate_signal()

    assert signal is None 


def test_news_strategy_buy_signal()
    # for normal case
    sentiments = [30, 45, 50, 80]  
    mock_news = MockNewsBook(sentiments)
    strat = NewsSentimentStrategy(mock_news, "AAPL")

    signal = None
    for _ in sentiments:
        signal = strat.generate_signal()

    assert signal is not None
    assert signal["signal"] == "BUY"
    assert signal["symbol"] == "AAPL"
    assert signal["sentiment"] >= 50


def test_news_strategy_no_buy_below_threshold():
    # for abnormal case

    sentiments = [20, 30, 49]
    mock_news = MockNewsBook(sentiments)
    strat = NewsSentimentStrategy(mock_news, "AAPL")

    for _ in sentiments:
        signal = strat.generate_signal()
        assert signal is None
