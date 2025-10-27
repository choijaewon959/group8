from strategies import BreakoutStrategy, MeanReversionStrategy
from observers import SignalPublisher, LoggerObserver, AlertObserver
from commands import ExecuteOrderCommand, Broker
from invokers import Invoker


def test_execute_order_command():
    broker = Broker()

    buy = ExecuteOrderCommand(broker,1,"AAPL",1,150)

    buy.execute()

    assert len(buy.broker.trades) == 1
    assert broker.trades[0] == (1, "AAPL", 1, 150)

def test_undo_order_command():
    broker = Broker()

    buy = ExecuteOrderCommand(broker, 1, "AAPL", 1, 150)

    buy.execute()
    buy.undo()

    assert len(broker.trades) == 2
    assert broker.trades[0][0] == 1
    assert broker.trades[1][0] == -1

def test_trade_lifecyle_using_invoker():
    invok = Invoker()
    broker = Broker()

    command = ExecuteOrderCommand(broker, 1, "AAPL", 1, 150)

    invok.execute_command(command)
    assert len(broker.trades) == 1
    assert broker.trades[-1] == (1, "AAPL", 1, 150)

    invok.undo_last()
    assert len(broker.trades) == 2
    assert broker.trades[-1] == (-1, "AAPL", 1, 150)

    invok.redo_last()
    assert len(broker.trades) == 3
    assert broker.trades[-1] == (1, "AAPL", 1, 150)



