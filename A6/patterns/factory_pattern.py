import csv
import datetime
from typing import List, Dict
from models import Instrument, Stock, Bond, ETF


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




