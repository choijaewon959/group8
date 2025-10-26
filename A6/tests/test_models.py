import os
import xml.etree.ElementTree as ET
import pytest
import json
from datetime import datetime
from models import MarketDataPoint, PortfolioGroup, Position


def _create_test_xml(file_path, entries):
    """Helper to create a fake Bloomberg XML file."""
    root = ET.Element("data")
    for e in entries:
        entry = ET.SubElement(root, "entry")
        ET.SubElement(entry, "symbol").text = e["symbol"]
        ET.SubElement(entry, "price").text = str(e["price"])
        ET.SubElement(entry, "timestamp").text = e["timestamp"]

    tree = ET.ElementTree(root)
    tree.write(file_path)


def _create_test_json(file_path, entries):
    """Helper to create a fake Yahoo Finance JSON file."""
    data = []
    for e in entries:
        data.append({
            "ticker": e["symbol"],
            "last_price": e["price"],
            "timestamp": e["timestamp"]
        })
    with open(file_path, 'w') as f:
        json.dump(data, f)


def test_get_data_returns_XML(mock_adapter_XML):
    xml_path = os.path.join(mock_adapter_XML.get_directory_path(), "external_data_bloomberg.xml")

    _create_test_xml(xml_path, [
        {"symbol": "AAPL", "price": 185.23, "timestamp": "2025-10-25T12:00:00"},
        {"symbol": "GOOG", "price": 2750.50, "timestamp": "2025-10-25T12:05:00"}
    ])

    result = mock_adapter_XML.get_data("GOOG")

    assert isinstance(result, MarketDataPoint)
    assert result.symbol == "GOOG"
    assert result.price == 2750.50
    assert result.timestamp == datetime.strptime("2025-10-25T12:05:00", "%Y-%m-%dT%H:%M:%S")


def test_get_data_file_not_found_XML(mock_adapter_XML):
    fake_path = os.path.join(mock_adapter_XML.get_directory_path(), "external_data_bloomberg.xml")
    if os.path.exists(fake_path):
        os.remove(fake_path)

    with pytest.raises(FileNotFoundError):
        mock_adapter_XML.get_data("AAPL")


def test_get_data_symbol_not_found_XML(mock_adapter_XML):
    xml_path = os.path.join(mock_adapter_XML.get_directory_path(), "external_data_bloomberg.xml")

    _create_test_xml(xml_path, [
        {"symbol": "MSFT", "price": 325.0, "timestamp": "2025-10-25T10:00:00"}
    ])

    result = mock_adapter_XML.get_data("AAPL")
    assert result is None 


def test_get_data_invalid_price_raises_XML(mock_adapter_XML):
    xml_path = os.path.join(mock_adapter_XML.get_directory_path(), "external_data_bloomberg.xml")

    _create_test_xml(xml_path, [
        {"symbol": "AAPL", "price": "BAD_NUM", "timestamp": "2025-10-25T12:00:00"}
    ])

    with pytest.raises(ValueError):
        mock_adapter_XML.get_data("AAPL")


def test_get_data_returns_json(mock_adapter_json):
    json_path = os.path.join(mock_adapter_json.get_directory_path(), "external_data_yahoo.json")

    _create_test_json(json_path, [
        {"symbol": "AAPL", "price": 185.23, "timestamp": "2025-10-25T12:00:00"},
    ])

    result = mock_adapter_json.get_data("AAPL")

    assert isinstance(result, MarketDataPoint)
    assert result.symbol == "AAPL"
    assert result.price == 185.23
    assert result.timestamp == datetime.strptime("2025-10-25T12:00:00", "%Y-%m-%dT%H:%M:%S")


def test_get_data_file_not_found_json(mock_adapter_json):
    fake_path = os.path.join(mock_adapter_json.get_directory_path(), "external_data_yahoo.json")
    if os.path.exists(fake_path):
        os.remove(fake_path)

    with pytest.raises(FileNotFoundError):
        mock_adapter_json.get_data("AAPL")


def test_get_data_symbol_not_found_json(mock_adapter_json):
    json_path = os.path.join(mock_adapter_json.get_directory_path(), "external_data_yahoo.json")

    _create_test_json(json_path, [
        {"symbol": "MSFT", "price": 325.0, "timestamp": "2025-10-25T10:00:00"}
    ])

    with pytest.raises(IndexError):
        mock_adapter_json.get_data("AAPL")


def test_portfolio_group():
    group = PortfolioGroup("Stock")

    AAPL_price = 150.0
    GOOG_price = 2500.0

    pos1 = Position("AAPL", 10, AAPL_price)
    pos2 = Position("GOOG", 5, GOOG_price)

    group.add_position(pos1)
    group.add_position(pos2)

    assert len(group.positions) == 2
    assert group.get_value() == pos1.get_value() + pos2.get_value()
    assert group.get_position() == pos1.get_position() + pos2.get_position()

