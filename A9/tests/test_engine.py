import unittest
from risk_engine import RiskEngine
from order import Order, OrderState

class TestRiskEngine(unittest.TestCase):

    def test_order_size_limit(self):
        # if order size exceed position --> false
        risk = RiskEngine(max_order_size=1000, max_position=2000)
        order = Order(symbol="AAPL", qty=1500, side="1")  # 1500 > 1000

        self.assertFalse(risk.check(order))

    def test_position_limit(self):
        # if current position + order > position--> false
        risk = RiskEngine(max_order_size=1000, max_position=2000)
        risk.positions["AAPL"] = 1800  

        order = Order(symbol="AAPL", qty=300, side="1")  

        self.assertFalse(risk.check(order))


    def test_update_position_buy(self):
        # Buy should increase a position size
        risk = RiskEngine()
        order = Order(symbol="AAPL", qty=300, side="1")  

        risk.update_position(order)
        self.assertEqual(risk.positions["AAPL"], 300)

    def test_update_position_sell(self):
        # Sell should decrease a position size
        risk = RiskEngine()
        risk.positions["AAPL"] = 500  

        order = Order(symbol="AAPL", qty=200, side="2")  # SELL

        risk.update_position(order)
        self.assertEqual(risk.positions["AAPL"], 300)  

