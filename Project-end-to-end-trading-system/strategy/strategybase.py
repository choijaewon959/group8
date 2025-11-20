from abc import ABC, abstractmethod

class StrategyBase(ABC):
    def __init__(self, position_size=1, strategy_name="BaseStrategy"):
        self.position_size = position_size
        self.strategy_name = strategy_name

    @abstractmethod
    def update_live_bar(self, row, ts=None):
        pass

    @abstractmethod
    def generate_live_signal(self):
        pass

    def reset(self):
        pass
