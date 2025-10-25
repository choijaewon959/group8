from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime.datetime
    symbol: str
    price: float

class Instrument(ABC):
    """
    금융 상품 추상 기본 클래스
    모든 금융 상품이 상속받는 부모 클래스
    """
    def __init__(self, symbol: str, instrument_type: str, price: float, sector:str, issuer: str):
        self.symbol = symbol
        self.type = instrument_type
        self.price = price
        self.sector = sector 
        self.issuer = issuer
    
    @abstractmethod  # 반드시 정의 되어야 하는 함수의 의미로 abstract method 사용 
    def get_price(self) -> float:
        """자산 가치 계산 (각 자산 타입별로 다르게 구현)"""
        pass
    
    @abstractmethod # 반드시 정의 되어야 하는 함수의 의미
    def get_info(self) -> dict:
        """자산 정보 반환"""
        pass
    
    def __repr__(self): # print 함수에 걸릴시 반환되는 값. 
        return f"{self.__class__.__name__}(symbol={self.symbol}, price={self.price})"


class Stock(Instrument):
    """
    주식 클래스 # type 자체가 Stock 즉 생성시 instrument_type에 Stock 이 들어간다. 
    """
    def __init__(self, symbol: str, price: float, sector: str, issuer: str):
        super().__init__(symbol, "Stock", price, sector, issuer) # super는 부모 생성자를 소환하는 생성자함수
    
    def update_price(self, md: MarketDataPoint):
        """틱 데이터로 주가 업데이트"""
        if md.symbol == self.symbol:
            self.price = md.price
            self.last_update = md.timestamp
    
    def get_price(self) -> float:
        """가장 최신 가격 = 현재 가격, price는 중요하니까 따로 빼주기."""
        return self.price
    
    def get_info(self) -> dict:
        """주식 정보 반환, price를 제외하고 전부 딕셔너리에 넣기"""
        return {
            'symbol': self.symbol,
            'type': self.type,
            'sector': self.sector,
            'issuer': self.issuer,
            'last_update':self.last_update
        }
    
    def __repr__(self):
        return f"Stock(symbol={self.symbol}, price={self.price}, sector={self.sector})"


class Bond(Instrument):
    """
    채권 클래스
    """
    def __init__(self, # 2025-10-01 ~ 2025-10-02 하루치니까 기본값 부여 
                 symbol: str = 'US10Y',  
                 sector: str = 'Government', 
                 issuer: str = 'US Treasury',  
                 maturity: datetime.datetime = datetime.datetime(2035, 10, 1), 
                 price: float = 100.0):
        super().__init__(symbol, "Bond", price, sector, issuer) # 부모 클래스 생성자로 생성하고
        self.maturity = maturity  # 별도의 속성은 따로 생성(정의)해주기
    
    
    def get_price(self) -> float:
        """가장 최신 가격을 가지고 있어야 하는데, 틱이 사실상 존재하지 않을거라서, 액면가 그대로 사용한다."""
        return self.price         # 애초 market_data.csv가 하루 2025-10-01 ~ 2025-10-02 하루사이의 기간이기 때문에 
                                  # US10Y : 채권 자체의 데이터가 존재하지 않는다. (적당한 임의값으로 par value 채권으로 간주하면 될듯!)
                                  # 즉, market_data.csv 가 아니라, instrument.csv 파일에 있는 값 그대로 넣어서 생성해보리면 될듯! 
    
    def get_info(self) -> dict:
        """채권 정보 반환"""
        return {
            'symbol': self.symbol,
            'type': self.type,
            'sector': self.sector,
            'issuer': self.issuer,
            'maturity': self.maturity
        }
    
    def __repr__(self):
        return f"Bond(symbol={self.symbol}, price={self.price}, maturity={self.maturity})"


class ETF(Instrument):
    """
    상장지수펀드(ETF) 클래스
    """
    def __init__(self, 
                 price: float,
                 symbol: str = 'SPY', 
                 sector: str = 'Index', 
                 issuer: str = 'State Street'):
    
        super().__init__(symbol, "ETF", price, sector, issuer)
        self.sector = sector

    def update_price(self, md: MarketDataPoint):
        """틱 데이터로 주가 업데이트""" 
        if md.symbol == self.symbol:
            self.price = md.price
            self.last_update = md.timestamp

    def get_price(self) -> float:
        """ETF 최신 가격(마지막가격)"""
        return self.price
    
    def get_info(self) -> dict:
        """ETF 정보 반환"""
        return {
            'symbol': self.symbol,
            'type': self.type,
            'sector': self.sector,
            'issuer': self.issuer,
            'last_update':self.last_update
        }
    
    def __repr__(self):
        return f"ETF(symbol={self.symbol}, price={self.price}, sector={self.sector})"


# class OrderStatus(Enum):
#     UNFILLED = "UNFILLED"
#     FILLED = "FILLED"
#     CANCELLED = "CANCELLED"

# class OrderAction(Enum):
#     BUY = "BUY"
#     SELL = "SELL"
#     HOLD = "HOLD"

# class OrderError(Exception):
#     pass

# class ExecutionError(Exception):
#     pass    

# class Order:
#     def __init__(self, timestamp: datetime, symbol: str, quantity: float, price: float, status: str, action: str, strategy: str):
#         if quantity <= 0:
#             raise OrderError("Quantity must be positive")
#         if price <= 0:
#             raise OrderError("Price must be positive")
#         if not symbol or not isinstance(symbol, str):
#             raise OrderError("Symbol must be a non-empty string")
#         if status not in [ os.value for os in OrderStatus ]:
#             raise OrderError("Invalid order status")

#         self.timestamp = timestamp
#         self.symbol = symbol
#         self.quantity = quantity
#         self.price = price
#         self.status = status
#         self.action = action
#         self.strategy = strategy

#     def __repr__(self):
#         return f"Order(symbol={self.symbol}, quantity={self.quantity}, price={self.price}, status={self.status}, action={self.action}, strategy={self.strategy})"




# # Portfolio 관련 클래스 (Builder Pattern에서 사용)
# class Position:
#     """
#     포트폴리오 내 개별 포지션 (보유 자산)
#     """
#     def __init__(self, symbol: str, quantity: int, price: float):
#         self.symbol = symbol
#         self.quantity = quantity
#         self.price = price
    
#     def get_value(self) -> float:
#         """포지션 가치 = 수량 × 가격"""
#         return self.quantity * self.price
    
#     def __repr__(self):
#         return f"Position(symbol={self.symbol}, qty={self.quantity}, value={self.get_value()})"


# class Portfolio:
#     """
#     포트폴리오 클래스 (Builder Pattern에서 조립될 객체)
#     """
#     def __init__(self):
#         self.owner: Optional[str] = None
#         self.positions: list[Position] = []
#         self.subportfolios: dict[str, 'Portfolio'] = {}
    
#     def get_total_value(self) -> float:
#         """전체 포트폴리오 가치 계산"""
#         total = sum(pos.get_value() for pos in self.positions)
#         total += sum(sub.get_total_value() for sub in self.subportfolios.values())
#         return total
    
#     def get_positions(self) -> list[Position]:
#         """모든 포지션 반환"""
#         return self.positions
    
#     def __repr__(self):
#         return f"Portfolio(owner={self.owner}, positions={len(self.positions)}, value={self.get_total_value()})"
