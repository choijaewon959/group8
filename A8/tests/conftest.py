import pytest
import socket
import threading

@pytest.fixture
def test_ports():
    return {
        'main': 9000,
        'alt1': 9001, 
        'alt2': 9002
    }

@pytest.fixture
def sample_messages():
    return {
        'register': 'REGISTER,STRATEGY,test_client_001',
        'price': 'PRICE,1609459200.123,AAPL,150.25,tick_001',
        'news': 'NEWS_SENTIMENT,1609459200.456,AAPL,0.75'
    }