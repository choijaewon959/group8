import pytest
import tempfile
from unittest.mock import MagicMock
from data_loader import BloombergXMLAdapter, YahooFinanceAdapter

@pytest.fixture
def mock_adapter_XML():
    """Fixture to return a BloombergXMLAdapter instance with a mocked data directory."""
    adapter = BloombergXMLAdapter()
    adapter.get_directory_path = MagicMock(return_value=tempfile.gettempdir())
    return adapter

@pytest.fixture
def mock_adapter_json():
    adapter = YahooFinanceAdapter()
    adapter.get_directory_path = MagicMock(return_value=tempfile.gettempdir())
    return adapter