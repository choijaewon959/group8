from abc import ABC, abstractmethod

class OrderCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Broker():
    def __init__(self):
        self.trades = []

    def execute_order(self,side,symbol,qty,price):
        self.trades.append((side,symbol,qty,price))
        label = "BUY" if side == 1 else "SELL"
        print(f"[BROKER] EXECUTED {label} signal for {qty} {symbol} at {price}")

    def reverse_order(self,side,symbol,qty,price):
        self.trades.append((-side,symbol,qty,price))
        label = "BUY" if side == 1 else "SELL"
        print(f"[BROKER] REVERSED {label} signal for {qty} {symbol} at {price}")


class ExecuteOrderCommand(OrderCommand):
    def __init__(self,broker,side,symbol,qty,price):
        self.broker = broker
        self.side = side
        self.symbol = symbol
        self.qty = qty
        self.price = price

    def execute(self):
        self.broker.execute_order(self.side,self.symbol,self.qty,self.price)

    def undo(self):
        self.broker.reverse_order(self.side,self.symbol,self.qty,self.price)


class UndoOrderCommand(OrderCommand):
    def __init__(self, broker, command):
        self.broker = broker
        self.command = command

    def execute(self):
        pass

    def undo(self):
        if self.command:
            self.command.undo()

