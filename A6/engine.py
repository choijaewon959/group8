from typing import Dict, List
from models import MarketDataPoint
from patterns.strategies import Strategy
from patterns.builder_pattern import Portfolio, PortfolioBuilder

class ExecutionEngine:
    def __init__(self, market_data: List[MarketDataPoint], strategies: dict):
        """
        market_data: csv file itself : contail mixed symbols
        """
        self.strategies: Dict[str, Strategy] = strategies
        self.portfolio: Dict[str, dict] = {}

        for strategy_name, strategy in self.strategies.items():
            builder = PortfolioBuilder(f"{strategy_name} Portfolio", owner="group8")
            self.portfolio[strategy_name] = builder.build()

        self.market_data = market_data

    def generate_all_signals(self, symbol: str):
        """
        set specific symbol and generate signals
        """
        all_signals = {}
        symbol_data = [tick for tick in self.market_data if tick.symbol == symbol]

        for strategy_name, strategy in self.strategies.items():
            signals = []
            for tick in symbol_data:
                sig = strategy.generate_signals(tick)
                if sig: 
                    signals.append(sig)
            all_signals[strategy_name] = signals

        return all_signals


    def apply_signals_to_portfolio(self, strategy_name, signals):
        portfolio = self.portfolio[strategy_name]
        positions = portfolio.get("positions", [])

        for sig in signals:
            existing = next((p for p in positions if p["symbol"] == sig["symbol"]), None)
            if existing:
                total_qty = existing["quantity"] + sig["qty"]
                existing["price"] = round((existing["price"]*existing["quantity"] + sig["price"]*sig["qty"])/total_qty, 4)
                existing["quantity"] = total_qty
            else:
                positions.append({"symbol": sig["symbol"], "quantity": sig["qty"], "price": sig["price"]})

        portfolio["positions"] = positions
        self.portfolio[strategy_name] = portfolio
