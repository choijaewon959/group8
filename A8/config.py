from enum import Enum

# Server Info
SERVER_HOST = "localhost"
SERVER_PORT_GATEWAY = 8999

# Message Info
BYTE_LIMIT = 1024
MESSAGE_DELIMITER = b'*'
STRING_DELIMITER = ','

# Message Type
class MessageType(Enum):
    REGISTER = "REGISTER"
    PRICE = "PRICE"
    NEWS_SENTIMENT = "NEWS_SENTIMENT"

# Client Type
class ClientType(Enum):
    STRATEGY = "STRATEGY"
    ORDERBOOK = "ORDERBOOK"