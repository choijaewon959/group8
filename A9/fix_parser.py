class FixParser:
    def __init__(self):
        pass

    @staticmethod
    def field_validator(func):
        def wrapper(self, msg):
            fields = func(self, msg)
            
            required_fields = []
            if fields['35'] == 'D':  # Order Message
                required_fields = ['8', '35', '55', '54', '38', '40', '10']
            elif fields['35'] == 'R':  # Quote Request Message
                required_fields = ['8', '35', '49', '56', '34', '52', '131', '55', '54', '10']
            elif fields['35'] == 'S':  # Quote Message
                required_fields = ['8', '35', '49', '56', '34', '52', '131', '117', '55', '132', '133', '134', '135', '10']

            for rf in required_fields:
                if rf not in fields:
                    raise ValueError(f"Missing required field: {rf}")
            return fields
        return wrapper

    @field_validator
    def parse(self, msg):
        fields = msg.split('|')
        parsed = {}
        for field in fields:
            if '=' in field:
                key, value = field.split('=', 1)
                parsed[key] = value
        return parsed


if __name__ == "__main__":
    msg_order = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128" # order
    msg_quote_request = "8=FIX.4.2|35=R|49=CLIENT1|56=DEALER1|34=2|52=20250116-23:59:59|131=REQ123|55=AAPL|54=1|10=123" # quote request
    msg_quote = "8=FIX.4.2|35=S|49=DEALER1|56=CLIENT1|34=3|52=20250116-23:59:59|131=REQ123|117=Q12345|55=AAPL|132=150.25|133=150.30|134=200|135=250|10=231" # quote

    parser = FixParser()
    fields = parser.parse(msg_order)
    print('order FIX: ', fields)

    fields = parser.parse(msg_quote_request)
    print('quote request FIX: ', fields)

    fields = parser.parse(msg_quote)
    print('quote FIX: ', fields)