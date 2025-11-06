def test_register_message_serialization():
    """Test REGISTER message format and serialization."""
    client_type = "STRATEGY"
    client_id = "test_client_001"
    message = f"REGISTER,{client_type},{client_id}"
    
    # Test serialization to bytes
    serialized = message.encode()
    assert isinstance(serialized, bytes)
    
    # Test deserialization back to string
    deserialized = serialized.decode()
    assert deserialized == message
    
    # Test message format
    parts = deserialized.split(',')
    assert len(parts) == 3
    assert parts[0] == "REGISTER"
    assert parts[1] == client_type
    assert parts[2] == client_id

def test_price_message_serialization():
    timestamp = "1609459200.123"
    symbol = "AAPL"
    price = "150.25"
    tick_id = "tick_001"
    message = f"PRICE,{timestamp},{symbol},{price},{tick_id}"
    
    # Test serialization to bytes
    serialized = message.encode()
    assert isinstance(serialized, bytes)
    
    # Test deserialization
    deserialized = serialized.decode()
    assert deserialized == message
    
    # Test message format
    parts = deserialized.split(',')
    assert len(parts) == 5
    assert parts[0] == "PRICE"
    assert parts[1] == timestamp
    assert parts[2] == symbol
    assert parts[3] == price
    assert parts[4] == tick_id

def test_message_buffer_handling():
    delimiter = '*'
    
    # Test single complete message
    message = f"REGISTER,STRATEGY,client001{delimiter}"
    if message.endswith(delimiter):
        extracted = message.rstrip(delimiter)
        assert extracted == "REGISTER,STRATEGY,client001"
    
    # Test multiple messages in buffer
    messages = f"REGISTER,STRATEGY,client001{delimiter}PRICE,123,AAPL,150{delimiter}"
    parts = messages.split(delimiter)
    complete_messages = [part for part in parts if part]
    
    assert len(complete_messages) == 2
    assert complete_messages[0] == "REGISTER,STRATEGY,client001"
    assert complete_messages[1] == "PRICE,123,AAPL,150"