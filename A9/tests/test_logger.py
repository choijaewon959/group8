from logger import Logger
import os
import json
import pytest


def test_check_coherent_logs(capsys):
    Mock_order = {"symbol" : "AAPL", "qty": 100}

    logger_obj = Logger("test.json")

    logger_obj.log("OrderCreated", Mock_order)
    #test order creation
    assert logger_obj.events[0] == {"type": "OrderCreated", "data":Mock_order}


    logger_obj.log("OrderAcked", Mock_order)
    #number of orders
    assert len(logger_obj.events) == 2
    #test order acked
    assert logger_obj.events[1] == {"type": "OrderAcked", "data":Mock_order}


    logger_obj.log("OrderUnknown", Mock_order)

    printer = capsys.readouterr().out
    #test printer captures unknown type
    assert "Unknown event type" in printer
    assert logger_obj.events[2]["type"] == "OrderUnknown"

    #create log file
    logger_obj.save()

    assert os.path.exists("test.json")

    with open("test.json", "r") as f:
        saved = json.load(f)

    #number of events should amount to what was saved
    assert saved == logger_obj.events

    #test new logger instance
    logger_obj2 = Logger("test.json")

    #test if singleton only instantiates once
    assert logger_obj is logger_obj2

