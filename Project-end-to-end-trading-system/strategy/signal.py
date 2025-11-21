class Signal:
    def __init__(self, action, qty, timestamp=None, price=None, strategy_name=None):
        """
        action: "BUY", "SELL", "HOLD"
        qty: integer
        timestamp: gateway's date index
        price: float 
        strategy_name: string
        """
        self.action = action
        self.qty = qty
        self.timestamp = timestamp
        self.price = price
        self.strategy_name = strategy_name
        
    def __repr__(self):
        return (
            f"Signal(ts={self.timestamp}, action={self.action}, "
            f"qty={self.qty}, strategy={self.strategy_name})"
        )
