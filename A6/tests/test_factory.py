import pytest
from patterns.factory_pattern import InstrumentFactory
from models import Stock, Bond, ETF
from patterns.builder_pattern import PortfolioBuilder

def test_create_stock():
    data = {
        "type": "Stock",
        "symbol": "AAPL",
        "price": 150,
        "sector": "Tech",
        "issuer": "Apple"
    }
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, Stock)
    assert inst.symbol == "AAPL"
    assert inst.price == 150
    assert inst.sector == "Tech"
    assert inst.issuer == "Apple"

def test_create_bond():
    data = {
        "type": "Bond",
        "symbol": "US10Y",
        "price": 100,
        "sector": "Government",
        "issuer": "US Treasury",
        "maturity": "2033-01-01"
    }
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, Bond)
    assert inst.symbol == "US10Y"
    assert inst.price == 100
    assert inst.sector == "Government"
    assert inst.issuer == "US Treasury"
    assert inst.maturity == "2033-01-01"

def test_create_etf():
    data = {
        "type": "ETF",
        "symbol": "SPY",
        "price": 430,
        "sector": "Index",
        "issuer": "SPDR"
    }
    inst = InstrumentFactory.create_instrument(data)
    assert isinstance(inst, ETF)
    assert inst.symbol == "SPY"
    assert inst.price == 430
    assert inst.sector == "Index"
    assert inst.issuer == "SPDR"

def test_create_invalid_type():
    data = {
        "type": "Crypto",
        "symbol": "BTC",
        "price": 40000
    }
    with pytest.raises(ValueError):
        InstrumentFactory.create_instrument(data)

def test_portfolio_builder_simple():
    builder = PortfolioBuilder("Test Portfolio", "tester")
    builder.add_position("AAPL", 100, 150)
    portfolio = builder.build()
    assert portfolio["name"] == "Test Portfolio"
    assert portfolio["owner"] == "tester"
    assert portfolio["positions"][0]["symbol"] == "AAPL"
    assert portfolio["positions"][0]["quantity"] == 100

def test_portfolio_builder_with_subportfolio():
    main = PortfolioBuilder("Main", "owner1").add_position("MSFT", 50, 300)
    sub = PortfolioBuilder("Sub", "owner2").add_position("SPY", 20, 430).portfolio  
    main.add_subportfolio(sub)  
    portfolio = main.build()    
    
    assert len(portfolio["sub_portfolios"]) == 1
    assert portfolio["sub_portfolios"][0]["name"] == "Sub"
