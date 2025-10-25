class Portfolio:
    def __init__(self, port_name: str, owner:str):
        self.port_name = port_name
        self.owner: str = owner
        self.positions: list[dict] = []
        self.sub_portfolios: list["Portfolio"] = []

    def get_value(self) -> float:
        total = sum(p["quantity"] * p["price"] for p in self.positions)
        total += sum(sub.get_value() for sub in self.sub_portfolios)
        return total

class PortfolioBuilder:
    def __init__(self, port_name: str, owner:str):
        self.portfolio = Portfolio(port_name, owner)

    def add_position(self, symbol: str, quantity: float, price: float):
        # currently add with order ??? 
        # or accumulated it at once?
        self.portfolio.positions.append({"symbol": symbol, "quantity": quantity, "price": price})
        return self

    def add_subportfolio(self, subportfolio: "Portfolio"):
        self.portfolio.sub_portfolios.append(subportfolio)
        return self

    def build(self) -> dict:    # print out function
        def portfolio_to_dict(p: Portfolio) -> dict:
            return {
                "name": p.port_name,
                "owner": p.owner,
                "positions": p.positions,
                "sub_portfolios": [portfolio_to_dict(sub) for sub in p.sub_portfolios]
            }
        return portfolio_to_dict(self.portfolio)

## Sample Execution
main_builder = PortfolioBuilder("Main Portfolio","doohwan1")\
    .add_position("AAPL", 100, 172.35)\
    .add_position("MSFT", 50, 328.10)

index_sub = PortfolioBuilder("Index Holdings","doohwan2")\
    .add_position("SPY", 20, 430.50)\
    .portfolio  # dictionary form same as json

print(main_builder.portfolio)

main_builder.add_subportfolio(index_sub)
portfolio_dict = main_builder.build()
print(portfolio_dict)
