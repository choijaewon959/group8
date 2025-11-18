from enum import Enum, auto

class OrderState(Enum): 
    NEW = auto() # 1st status
    ACKED = auto() # 2nd status
    FILLED = auto() # 3rd status
    CANCELED = auto() # 3rd status
    REJECTED = auto() # 2nd status

class Order:
    def __init__(self, symbol, qty, side):
        self.state = OrderState.NEW
        self.symbol = symbol
        self.qty = qty
        self.side = side                  # side should be '+1' or '-1'
        self.state = OrderState.NEW

    def transition(self, new_state):
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
        }

        if new_state in allowed.get(self.state, {}):
            print(f"[OK] {self.state.name} → {new_state.name}")
            self.state = new_state
        else:
            print(f"[ERROR] Invalid transition: {self.state.name} → {new_state.name}")
    

