class RiskEngine:
    def __init__(self, max_order_size=1000, max_position=2000):
        self.max_order_size = max_order_size
        self.max_position = max_position
        self.positions = {}   # load current positions with symbols

    def check(self, order) -> bool:
        symbol = order.symbol
        qty = order.qty

        # 1) check order size 
        if qty > self.max_order_size:
            print(f"[RISK] Order rejected: size too large ({qty} > {self.max_order_size})")
            return False

        # 2) check current position 
        current_pos = self.positions.get(symbol, 0)
        # order have side as '+1' or '-1'
        direction = 1 if order.side == "1" else -1
        new_pos = current_pos + direction * qty

        # 3) check position limit
        if abs(new_pos) > self.max_position:
            print(f"[RISK] Order rejected: position limit exceeded for {symbol}.")
            return False

        return True 

    def update_position(self, order):
        symbol = order.symbol
        qty = order.qty
        direction = 1 if order.side == "1" else -1
        
        current_pos = self.positions.get(symbol, 0)
        new_pos = current_pos + direction * qty

        self.positions[symbol] = new_pos
        print(f"[RISK] Updated position: {symbol} = {new_pos}")
