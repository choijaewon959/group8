import json

class Logger:
    __instance = None
    __initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, path="events.json"):
        if not Logger.__initialized:
            self.logfile = path
            self.events = []
            Logger.__initialized = True

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


if __name__ == "main":
    log1 = Logger("test.json")
    log2 = Logger("hello.json")

    print(log1 is log2)








