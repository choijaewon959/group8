import socket
from orderbook import SharedPriceBook
import time
import pytest
from multiprocessing import Process, shared_memory
from shared_memory_utils import get_memory_footprint_mb


def writer_process(symbols, shared_mem_name, symbol, value):
    book = SharedPriceBook(symbols, shared_mem_name, create=False)
    book.update(symbol, value)
    time.sleep(0.2)

def test_shared_memory_propagates_updates():

    symbols = ["AAPL", "MSFT"]
    shared_mem_name = "test_shared_memory"

    writer_book = SharedPriceBook(symbols, shared_mem_name, create=True)
    reader_book = SharedPriceBook(symbols, shared_mem_name, create=False)

    writer_book.update("AAPL",150)
    assert writer_book.read("AAPL") == 150

    p = Process(target=writer_process, args=(symbols, shared_mem_name, "MSFT",400))
    p.start()
    p.join()

    time.sleep(0.1)

    updated_val = reader_book.read("MSFT")

    assert updated_val == 400

    footprint = get_memory_footprint_mb(shared_mem_name)
    assert footprint < 1

    reader_book.shm.close()
    writer_book.shm.close()
    writer_book.shm.unlink()









