import os
import xml.etree.ElementTree as ET
import pandas as pd
import csv
from abc import ABC, abstractmethod
from datetime import datetime
from models import MarketDataPoint


'''
    Adapter Pattern Implementation
'''
class MarketDataSource(ABC):
    @abstractmethod
    def get_data(self, symbol) -> MarketDataPoint:
        pass

    def get_directory_path(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "./", "data"))
    

class CSVAdapter(MarketDataSource):
    def get_data(self, symbol) -> MarketDataPoint:
        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, "instruments.csv")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"CSV file not found: {data_path}")

        instruments = []
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["symbol"] != symbol:
                    continue

                data = {
                    "symbol": row["symbol"],
                    "type": row["type"],
                    "price": float(row["price"]),
                    "sector": row.get("sector", "Unknown"),
                    "issuer": row.get("issuer", "Unknown"),
                }
                if row["type"] == "Bond" and row.get("maturity"):
                    data["maturity"] = datetime.strptime(row["maturity"], "%Y-%m-%d")
                instruments.append(data)
        return instruments
    
    def get_market_data(self):
        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, "market_data.csv")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"CSV file not found: {data_path}")

        market_data = []
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_point = MarketDataPoint(
                    timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    symbol=row["symbol"],
                    price=float(row["price"])
                )
                market_data.append(data_point)
        return market_data


class BloombergXMLAdapter(MarketDataSource):
    def get_data(self, symbol) -> MarketDataPoint:
        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, "external_data_bloomberg.xml")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"XML file not found: {data_path}")
        
        # Parse XML and check if symbol matches
        tree = ET.parse(data_path)
        root = tree.getroot()

        # Handle multiple entries - look for the matching symbol
        for entry in root.findall('.//entry'):
            xml_symbol = entry.findtext("symbol")
            if xml_symbol == symbol:
                xml_timestamp = datetime.strptime(entry.findtext("timestamp"), "%Y-%m-%dT%H:%M:%S")
                xml_price = float(entry.findtext("price"))
                return MarketDataPoint(xml_timestamp, xml_symbol, xml_price)


class YahooFinanceAdapter(MarketDataSource):
    def get_data(self, symbol) -> MarketDataPoint:
        data_dir = self.get_directory_path()
        data_path = os.path.join(data_dir, "external_data_yahoo.json")

        df = pd.read_json(data_path)
        df = df[df['ticker'] == symbol]

        row = df.iloc[0]   
        return MarketDataPoint(row['timestamp'], row['ticker'], row['last_price'])