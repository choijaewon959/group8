from asyncio import new_event_loop
from patterns.observers import Observer
from datetime import datetime
import json
import csv


class reportObserver(Observer):
    def __init__(self):
        self.signals = []
        self.historic = {"Total signals" : 0,
                      "Buy signals": 0,
                      "Sell signals": 0,
                      "average price": 0}

    def update(self, signal:dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        signal =  {'time': timestamp,
               'strategy': signal['strategy'],
               'symbol': signal['symbol'],
               'quantity': 1,
               'price': signal['price'],
               'signal': signal['signal']}

        self.signals.append(signal)

        self.historic['Total signals'] += 1
        if signal['signal'] == 1:
            self.historic['Buy signals'] += 1
        elif signal['signal'] == -1:
            self.historic['Sell signals'] += 1

        self.historic['average price'] += (signal['price'] - self.historic['average price'])/self.historic['Total signals']

        print(f"[REPORT] ADDED {signal['signal']} signal for {signal['symbol']} at {signal['price']} with {signal['strategy']}")

    def summary(self) -> dict:
        summary = self.historic.copy()
        summary["latest signal"] = self.signals[-1] if self.signals else None
        return summary

    def to_json(self, filename = "report.json"):
        with open(filename, "w") as f:
            json.dump(self.signals, f)
        print(f"[REPORT] Wrote JSON to {filename}")

    def to_csv(self, filename = "report.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.signals[0].keys())
            writer.writeheader()
            writer.writerows(self.signals)
        print(f"[REPORT] Wrote CSV to {filename}")






