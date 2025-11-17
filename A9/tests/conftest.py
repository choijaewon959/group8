import pytest


@pytest.fixture
def sample_fix_message():
    return {
        'order': "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128",
        'quote_request': "8=FIX.4.2|35=R|49=DUMMYCLIENT|56=DUMMYDEALER|34=2|52=20250116-23:59:59|131=REQ123|55=AAPL|54=1|10=123",
        'quote': "8=FIX.4.2|35=S|49=DUMMYCLIENT|56=DUMMYDEALER|34=3|52=20250116-23:59:59|131=REQ123|117=Q12345|55=AAPL|132=150.25|133=150.30|134=200|135=250|10=231"
    }


@pytest.fixture
def bad_fix_message():
    return {
        'missing_order': "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|10=128",  # Missing 40
        'missing_quote_request': "8=FIX.4.2|35=R|49=DUMMYCLIENT|56=DUMMYDEALER|34=2|52=20250116-23:59:59|55=AAPL|54=1|10=123",  # Missing 131
        'missing_quote': "8=FIX.4.2|35=S|49=DUMMYCLIENT|56=DUMMYDEALER|34=3|52=20250116-23:59:59|117=Q12345|55=AAPL|132=150.25|133=150.30|134=200|10=231"  # Missing 131 and 135
    }

