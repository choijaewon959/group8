import csv
from dataclasses import dataclass
import datetime
from typing import List, Dict
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
import datetime


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
                 maturity: datetime.datetime = datetime.datetime(2035, 10, 1), 
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


class InstrumentFactory:
    @staticmethod
    def create_instrument(data: Dict) -> Instrument:
        type_ = data["type"]
        if type_ == "Stock":
            return Stock(
                symbol=data["symbol"],
                price=data["price"],
                sector=data["sector"],
                issuer=data["issuer"]
            )
        elif type_ == "Bond":
            return Bond(
                symbol=data["symbol"],
                price=data.get("price", 100.0),
                sector=data.get("sector", "Government"),
                issuer=data.get("issuer", "US Treasury"),
                maturity=data.get("maturity") 
            )
        elif type_ == "ETF":
            return ETF(
                symbol=data["symbol"],
                price=data["price"],
                sector=data["sector"],
                issuer=data["issuer"]
            )
        else:
            raise ValueError(f"Unknown instrument type: {type_}")


def load_instruments_csv(file_path: str) -> List[Dict]:
    instruments = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {
                "symbol": row["symbol"],
                "type": row["type"],
                "price": float(row["price"]),
                "sector": row.get("sector", "Unknown"),
                "issuer": row.get("issuer", "Unknown"),
            }
            if row["type"] == "Bond" and row.get("maturity"):
                data["maturity"] = datetime.datetime.strptime(row["maturity"], "%Y-%m-%d")
            instruments.append(data)
    return instruments


# Sample Execution
raw_instruments = load_instruments_csv("data/instruments.csv")

# divide by symbol 
symbol_map = {}
for d in raw_instruments:
    obj = InstrumentFactory.create_instrument(d)
    symbol_map[d["symbol"]] = obj

AAPL_stock = symbol_map.get("AAPL")
MSFT_stock = symbol_map.get("MSFT")
US10Y_bond = symbol_map.get("US10Y")
SPY_etf = symbol_map.get("SPY")

print(AAPL_stock.get_info())
print(US10Y_bond.get_info())
print(SPY_etf.get_info())
