from models import Stock, Bond, ETF, Instrument
from typing import Dict

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


class PortfolioBuilder:
    def __init__(self, name: str):
        self.portfolio = {
            "name": name,
            "positions": [],
            "sub_portfolios": []
        }

    def set_owner(self, owner: str):
        self.portfolio["owner"] = owner
        return self

    def add_position(self, symbol: str, quantity: float, price: float):
        position = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price
        }
        self.portfolio["positions"].append(position)
        return self

    def add_subportfolio(self, name: str, builder: 'PortfolioBuilder'):
        self.portfolio["sub_portfolios"].append(builder.build())
        return self

    def build(self) -> Dict[str, Any]:
        return self.portfolio









###
from price_loader import load_instruments_csv#, load_market_data_csv
from pattern_factory import InstrumentFactory

# 이때 반환되는 값은 Dictionary로 csv파일 값 그자체 그대로 들고옴
raw_instruments = load_instruments_csv("instruments.csv")

instruments = [InstrumentFactory.create_instrument(d) for d in raw_instruments]

# market_data = load_market_data_csv("market_data.csv")
# 포트폴리오 json에 사용된거 그대로 써주기!
# portfolio_structure.json에 사용된거 그대로 쓰기! 뭔가 객체로 관리할 생각하지 말기! 
symbol_map = {inst.symbol: inst for inst in instruments}  # symbol → Instrument 매핑

# for mdp in market_data:
#     if mdp.symbol in symbol_map:
#         inst = symbol_map[mdp.symbol]
#         # Stock/ETF만 update_price 메서드 존재
#         if hasattr(inst, "update_price"):
#             inst.update_price(mdp)

for inst in instruments:
    print(inst)
    # if hasattr(inst, "last_update"):
    #     print("  Last update:", inst.last_update)
