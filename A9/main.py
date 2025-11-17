from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine

if __name__ == "__main__":
    # generate FIX Parser & Risk Engine 
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)

    # example of FIX message 
    raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
    msg = fix.parse(raw)

    print("\n[STEP] FIX MESSAGE PARSED")
    print(msg)

    # generate Order 
    order = Order(
        symbol=msg["55"],           # AAPL
        qty=int(msg["38"]),         # 500
        side=msg["54"]              # 1 (buy)
    )

    print(f"[STEP] ORDER CREATED: {order.symbol}, qty={order.qty}, side={order.side}, state={order.state.name}")

    # check risk margin
    print("\n[STEP] RUN RISK CHECK")
    if risk.check(order):
        order.transition(OrderState.ACKED)
    else:
        order.transition(OrderState.REJECTED)
        print("[END] Order rejected by risk engine.")
        exit()

    # Order transition log
    print("\n[STEP] ORDER FILLED")
    risk.update_position(order)
    order.transition(OrderState.FILLED)

    # final position log
    print("\n[STEP] FINAL POSITION")
    print(risk.positions)

