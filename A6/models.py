import datetime
import os
import xml.etree.ElementTree as ET
import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime.datetime
    symbol: str
    price: float


'''
    Adapter Pattern Implementation
'''
class MarketDataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass

    def get_directory_path(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "./", "data"))
    

class BloombergXMLAdapter(MarketDataSource):
    def get_data(self) -> MarketDataPoint:
        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, "external_data_bloomberg.xml")

        # Parse manually since the XML has only one <instrument> element
        tree = ET.parse(data_path)
        root = tree.getroot()  # <instrument>

        symbol = root.findtext("symbol")
        price = float(root.findtext("price"))
        timestamp = root.findtext("timestamp")

        return MarketDataPoint(timestamp, symbol, price)


class YahooFinanceAdapter(MarketDataSource):
    def get_data(self) -> MarketDataPoint:
        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, "external_data_yahoo.json")

        df = pd.read_json(data_path, typ="series").to_frame().T

        row = df.iloc[0]   
        return MarketDataPoint(row['timestamp'], row['ticker'], row['last_price'])


'''
    Composite Pattern Implementation
'''
class PortfolioComponent(ABC):
    @abstractmethod
    def get_value(self) -> float:
        pass   

    @abstractmethod
    def get_position(self) -> int:
        pass


class Position(PortfolioComponent):
    def __init__(self, symbol: str, quantity: int, price: float):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price

    def get_value(self) -> float:
        return self.quantity * self.price

    def get_position(self) -> int:
        return self.quantity


class PortfolioGroup(PortfolioComponent):
    def __init__(self, name: str):
        self.name = name
        self.components = []

    def add_component(self, component: PortfolioComponent):
        self.components.append(component)

    def get_value(self) -> float:
        return sum(c.get_value() for c in self.components)


    def get_position(self) -> int:
        return sum(c.get_position() for c in self.components)
