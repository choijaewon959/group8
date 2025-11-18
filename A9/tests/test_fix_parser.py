import pytest
from fix_parser import FixParser


def test_fix_parser(sample_fix_message):
    fp = FixParser()

    # Test Order Message
    order_msg = sample_fix_message['order']
    order_fields = fp.parse(order_msg)
    assert order_fields['35'] == 'D'
    assert order_fields['55'] == 'AAPL'
    assert order_fields['54'] == '1'
    assert order_fields['38'] == '100'
    assert order_fields['40'] == '2'
    assert order_fields['10'] == '128'

    # Test Quote Request Message
    quote_request_msg = sample_fix_message['quote_request']
    quote_request_fields = fp.parse(quote_request_msg)
    assert quote_request_fields['35'] == 'R'
    assert quote_request_fields['49'] == 'DUMMYCLIENT'
    assert quote_request_fields['56'] == 'DUMMYDEALER'
    assert quote_request_fields['34'] == '2'
    assert quote_request_fields['52'] == '20250116-23:59:59'
    assert quote_request_fields['131'] == 'REQ123'
    assert quote_request_fields['55'] == 'AAPL'
    assert quote_request_fields['54'] == '1'
    assert quote_request_fields['10'] == '123'

    # Test Quote Message
    quote_msg = sample_fix_message['quote']
    quote_fields = fp.parse(quote_msg)
    assert quote_fields['35'] == 'S'
    assert quote_fields['49'] == 'DUMMYCLIENT'
    assert quote_fields['56'] == 'DUMMYDEALER'
    assert quote_fields['34'] == '3'
    assert quote_fields['52'] == '20250116-23:59:59'
    assert quote_fields['131'] == 'REQ123'
    assert quote_fields['117'] == 'Q12345'
    assert quote_fields['55'] == 'AAPL'
    assert quote_fields['132'] == '150.25'
    assert quote_fields['133'] == '150.30'
    assert quote_fields['134'] == '200'
    assert quote_fields['135'] == '250'
    assert quote_fields['10'] == "231"


def test_fix_parser_missing_fields(bad_fix_message):
    fp = FixParser()

    # Test missing field in Order Message
    missing_order_msg = bad_fix_message['missing_order']
    with pytest.raises(ValueError):
        fp.parse(missing_order_msg)

    # Test missing field in Quote Request Message
    missing_quote_request_msg = bad_fix_message['missing_quote_request']
    with pytest.raises(ValueError):
        fp.parse(missing_quote_request_msg)

    # Test missing field in Quote Message
    missing_quote_msg = bad_fix_message['missing_quote']
    with pytest.raises(ValueError):
        fp.parse(missing_quote_msg)


def test_fix_parser_edge_cases():
    fp = FixParser()
    
    # Test field with equals sign in value (only split on first =)
    msg_with_special = "8=FIX.4.2|35=D|55=AA=PL|54=1|38=100|40=2|10=128"
    fields = fp.parse(msg_with_special)
    assert fields['55'] == 'AA=PL'
    
    # Test empty field handling
    msg_with_empty = "8=FIX.4.2|35=D|55=|54=1|38=100|40=2|10=128"
    fields = fp.parse(msg_with_empty)
    assert fields['55'] == ''
    
    # Test trailing pipe
    msg_with_trailing = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128|"
    fields = fp.parse(msg_with_trailing)
    assert fields['10'] == '128'
