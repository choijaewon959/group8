from patterns.observers import SignalPublisher, LoggerObserver, AlertObserver
import pytest

def test_notify_observers():
    signal = {"strategy": "BreakoutStrategy",
        "symbol": "MSFT",
        "signal": 1,
        "price": 150,
        "qty": 1}

    publisher = SignalPublisher()
    executed = []

    class obs:
        def update(self, signal):
            executed.append(signal)

    publisher.attach(obs())
    publisher.notify(signal)

    assert len(executed) == 1
    assert executed[0]["symbol"] == "MSFT"

def test_attaching_observers():
    signal = {"strategy": "BreakoutStrategy",
              "symbol": "MSFT",
              "signal": 1,
              "price": 150,
              "qty": 2}

    publisher = SignalPublisher()
    obs1, obs2 = [], []

    class Observer1:
        def update(self, signal):
            obs1.append(signal)

    class Observer2:
        def update(self, signal):
            obs2.append(signal)

    publisher.attach(Observer1())
    publisher.attach(Observer2())
    publisher.attach(Observer2())

    publisher.notify(signal)

    assert len(obs1) == 1
    assert len(obs2) == 2