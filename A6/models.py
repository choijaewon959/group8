from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float


'''
    Instruments Implementation
'''
class Instrument(ABC):
    def __init__(self, symbol: str, instrument_type: str, price: float, sector:str, issuer: str):
        self.symbol = symbol
        self.type = instrument_type
        self.price = price
        self.sector = sector 
        self.issuer = issuer
        
    @abstractmethod 
    def get_info(self) -> dict:
        pass


class Stock(Instrument):
    def __init__(self, symbol: str, price: float, sector: str, issuer: str):
        super().__init__(symbol, "Stock", price, sector, issuer) 
        
    def get_info(self) -> dict:
        return {
            'symbol': self.symbol,
            'type': self.type,
            'price': self.price,
            'sector': self.sector,
            'issuer': self.issuer,
        }
    

class Bond(Instrument):
    def __init__(self,  
                 symbol: str = 'US10Y',  
                 sector: str = 'Government', 
                 issuer: str = 'US Treasury',  
                 maturity: datetime = datetime(2035, 10, 1), 
                 price: float = 100.0):
        super().__init__(symbol, "Bond", price, sector, issuer) 
        self.maturity = maturity
    
    def get_info(self) -> dict:
        return {
            'symbol': self.symbol,
            'type': self.type,
            'price': self.price,
            'sector': self.sector,
            'issuer': self.issuer,
            'maturity': self.maturity
        }


class ETF(Instrument):
    def __init__(self, 
                 price: float,
                 symbol: str = 'SPY', 
                 sector: str = 'Index', 
                 issuer: str = 'State Street'):
    
        super().__init__(symbol, "ETF", price, sector, issuer)
        self.sector = sector
    
    def get_info(self) -> dict:
        return {
            'symbol': self.symbol,
            'type': self.type,
            'price': self.price,
            'sector': self.sector,
            'issuer': self.issuer,
        }


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
        self.positions = []

    def add_position(self, position: Position):
        self.positions.append(position)

    def get_value(self) -> float:
        return sum(c.get_value() for c in self.positions)

    def get_position(self) -> int:
        return sum(c.get_position() for c in self.positions)
