import sqlite3
import pandas as pd
import pytest
from pathlib import Path

from sqlite_storage import (
    create_schema,
    insert_tickers_data,
    insert_market_data,
    retrieve_market_data,
    calc_avg_daily_volume,
    get_top_performers,
    get_first_and_last_trade_price
)


@pytest.fixture
def fresh_db(tmp_path):
    db_path = tmp_path / "test_market.db"
    create_schema(db_path)
    return db_path


def test_schema_created(fresh_db):
    conn = sqlite3.connect(fresh_db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}

    assert "tickers" in tables
    assert "prices" in tables

    conn.close()


def test_insert_and_retrieve(fresh_db):
    insert_tickers_data(fresh_db, [
        (1, "AAPL", "Apple Inc", "NASDAQ"),
        (2, "TSLA", "Tesla", "NASDAQ")
    ])

    insert_market_data(fresh_db, [
        ("2025-11-17 09:30:00", 1, 100, 101, 99, 100, 1000),
        ("2025-11-17 09:35:00", 1, 101, 102, 100, 101, 1500),
        ("2025-11-17 09:30:00", 2, 200, 201, 199, 200, 2000)
    ])

    rows = retrieve_market_data(
        fresh_db,
        symbol=1,
        start_time="2025-11-17",
        end_time="2025-11-18"
    )

    assert len(rows) == 2 


def test_avg_daily_volume(fresh_db):
    insert_tickers_data(fresh_db, [(1, "AAPL", "Apple", "NASDAQ")])

    insert_market_data(fresh_db, [
        ("2025-11-17 09:30:00", 1, 100, 101, 99, 100, 1000),
        ("2025-11-17 09:35:00", 1, 101, 102, 100, 101, 1500),
    ])

    avg_vol = calc_avg_daily_volume(fresh_db)

    # One ticker, one date → AVG(volume) = (1000 + 1500) / 2 = 1250
    assert len(avg_vol) == 1
    assert avg_vol[0][0] == pytest.approx(1250.0)


def test_top_performers(fresh_db):
    insert_tickers_data(fresh_db, [(1, "AAPL", "Apple", "NASDAQ")])

    insert_market_data(fresh_db, [
        ("2025-11-17 09:30:00", 1, 100, 101, 99, 100, 1000),  # Day 1 close = 100
        ("2025-11-18 09:30:00", 1, 105, 106, 99, 105, 1000),  # Day 2 close = 105
    ])

    result = get_top_performers(
        fresh_db,
        n=1,
        start_time="2025-11-17",
        end_time="2025-11-18"
    )

    expected_return = (105 - 100) / 100 * 100  

    assert result[0][0] == pytest.approx(expected_return)


def test_first_last_trade_price(fresh_db):
    insert_tickers_data(fresh_db, [(1, "AAPL", "Apple", "NASDAQ")])

    insert_market_data(fresh_db, [
        ("2025-11-17 09:30:00", 1, 100, 101, 99, 100, 1000),
        ("2025-11-17 16:00:00", 1, 105, 106, 99, 105, 2000),
    ])

    rows = get_first_and_last_trade_price(fresh_db)

    assert len(rows) == 2
    assert rows[0][2] == "2025-11-17 09:30:00"
    assert rows[1][2] == "2025-11-17 16:00:00"
