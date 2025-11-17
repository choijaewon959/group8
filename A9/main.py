from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger

if __name__ == "__main__":
    # generate FIX Parser, Risk Engine & logger
    fix = FixParser()
    risk = RiskEngine(max_order_size=1000, max_position=2000)
    log = Logger()

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
    # log order creation
    log.log("OrderCreated", msg)

    print(f"[STEP] ORDER CREATED: {order.symbol}, qty={order.qty}, side={order.side}, state={order.state.name}")

    # check risk margin
    print("\n[STEP] RUN RISK CHECK")

    try:
        risk.check(order)
        order.transition(OrderState.ACKED)
        log.log("OrderAcked", {"symbol": order.symbol, "qty": order.qty})

    except ValueError as e:
        order.transition(OrderState.REJECTED)
        print("[END] Order rejected by risk engine.")
        log.log("OrderRejected", {"reason": str(e)})
        exit()

    # Order transition log
    print("\n[STEP] ORDER FILLED")
    risk.update_position(order)
    order.transition(OrderState.FILLED)
    log.log("OrderFilled", {"symbol": order.symbol, "qty": order.qty})

    # final position log
    print("\n[STEP] FINAL POSITION")
    print(risk.positions)

    log.save()

