import socket
from orderbook import SharedPriceBook

def test_shared_memory_propagates_updates():

    symbols = ["AAPL", "SPY"]
    shared_mem_name = "test_shared_memory"

    writer_book = SharedPriceBook(symbols, shared_mem_name, create=True)
    reader_book = SharedPriceBook(symbols, shared_mem_name, create=False)




