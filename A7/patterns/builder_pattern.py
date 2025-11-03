import pandas as pd


class Portfolio:
    def __init__(self, port_name: str, owner: str):
        self.port_name = port_name
        self.owner: str = owner
        self.positions: list[dict] = []
        self.sub_portfolios: list["Portfolio"] = []

    def get_value(self) -> float:
        total = sum(p["quantity"] * p["price"] for p in self.positions)
        total += sum(sub.get_value() for sub in self.sub_portfolios)
        return total

    def __repr__(self):
        return self._repr_recursive()

    def _repr_recursive(self, level=0):
        indent = "  " * level
        s = f"{indent}Portfolio: {self.port_name}, Owner: {self.owner}\n"
        for pos in self.positions:
            s += f"{indent}  Position: {pos}\n"
        for sub in self.sub_portfolios:
            s += sub._repr_recursive(level + 1)
        return s


class PortfolioBuilder:
    def __init__(self, port_name: str, owner: str):
        self.portfolio = Portfolio(port_name, owner)

    def add_position(self, symbol: str, quantity: float, price: float, ts: pd.DataFrame):

        self.portfolio.positions.append({"symbol": symbol, "quantity": quantity, "price": price, 'ts': ts})
        return self

    def add_subportfolio(self, subportfolio: "Portfolio"):

        subportfolio.__dict__.pop('sub_portfolios', None)
        subportfolio.__dict__.pop('owner', None)
        self.portfolio.sub_portfolios.append(subportfolio)
        return self

    def build(self) -> dict:
        def portfolio_to_dict(p, is_main=True):
            d = {"name": p.port_name}

            # 메인 포트일 경우만 owner 유지
            if is_main and hasattr(p, "owner") and p.owner is not None:
                d["owner"] = p.owner

            # positions 처리
            positions_list = []
            for pos in getattr(p, "positions", []):
                pos_dict = pos.copy()
                pos_dict.pop("ts", None)  # JSON에 시계열 제거
                positions_list.append(pos_dict)
            if positions_list:
                d["positions"] = positions_list

            # sub_portfolios 처리 (메인 포트일 때만 포함)
            if is_main and getattr(p, "sub_portfolios", []):
                sub_list = []
                for sub in p.sub_portfolios:
                    sub_dict = portfolio_to_dict(sub, is_main=False)
                    sub_list.append(sub_dict)
                if sub_list:
                    d["sub_portfolios"] = sub_list

            return d

        return portfolio_to_dict(self.portfolio)


