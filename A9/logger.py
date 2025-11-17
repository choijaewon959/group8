import json

class Logger:

    def __init__(self, path="events.json"):
        self.logfile = path
        self.events = []


    def log(self, event_type, data):
        self.events.append({"type":event_type, "data":data})

        if event_type == "OrderCreated":
            print(f"[LOG] OrderCreated -> {data}")

        elif event_type == "OrderAcked":
            print(f"Order {data['symbol']} is now ACKED")

        elif event_type == "OrderFilled":
            print(f"Order {data['symbol']} is now FILLED")
            print(f"[LOG] OrderFilled -> {data}")

        elif event_type == "OrderRejected":
            print(f"{data}: Order is now REJECTED")

        else:
            print(f"[WARN] Unknown event type: {event_type}")


    def save(self):
        with open(self.logfile, "w") as f:
            json.dump(self.events, f, indent=2)
            print(f"[LOG] saved {len(self.events)} events in {self.logfile}")









