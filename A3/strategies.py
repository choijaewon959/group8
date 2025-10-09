from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass