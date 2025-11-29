import sqlite3
import pandas as pd
from pathlib import Path
from data_loader import load_market_data, load_ticker_data

def table_exists(db_path: str, table_name: str) -> bool:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=?;
    """, (table_name,))

    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def create_schema(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    schema_sql = Path('schema.sql').read_text()
    cursor.executescript(schema_sql)
    
    conn.commit()
    conn.close()


def insert_tickers_data(db_path: str, data: list):
    conn = sqlite3.connect(db_path,timeout=30)
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO tickers (ticker_id, symbol, name, exchange)
        VALUES (?, ?, ?, ?)
    """

    cursor.executemany(insert_sql, data)
    
    conn.commit()
    conn.close()


def insert_market_data(db_path: str, data: list):
    conn = sqlite3.connect(db_path,timeout=30)
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO prices (timestamp, ticker_id, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.executemany(insert_sql, data)
    
    conn.commit()
    conn.close()


def retrieve_market_data(db_path: str, symbol: str, start_time: str, end_time: str):
    print(f"Retrieving market data for {symbol} from {start_time} to {end_time}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query_sql = """
        SELECT * 
        FROM prices
        WHERE ticker_id = ?
        AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    """

    cursor.execute(query_sql, (symbol, start_time, end_time))
    rows = cursor.fetchall()
    
    conn.close()
    return rows


def calc_avg_daily_volume(db_path: str) -> float:
    print("Calculating average daily volume...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query_sql = """
        SELECT AVG(volume) AS avg_daily_volume, ticker_id, DATE(timestamp) AS trade_date
        FROM prices
        GROUP BY ticker_id, DATE(timestamp)
    """

    cursor.execute(query_sql)
    avg_volume = cursor.fetchall()
    
    conn.close()
    return avg_volume


def get_top_performers(db_path: str, n: int = 3, start_time: str = None, end_time: str = None):
    """
        Retrieves top N performing tickers based on percentage price change between start_time and end_time.
        start_time and end_time should be in 'YYYY-MM-DD' format, and is assumed to be correctly aligned with trading days in db.
        This gets the last close price for first day and close price for last day for each ticker to calculate performance.
    """
    print("Retrieving top performers...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    day_after_first = (pd.Timestamp(start_time) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    day_after_last = (pd.Timestamp(end_time) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')

    query_sql = """
        WITH 
        first_price AS (
            SELECT p.ticker_id as ticker, p.close AS last_close, p.timestamp
            FROM prices p
            JOIN (
                SELECT ticker_id as ticker, MAX(timestamp) AS max_ts
                FROM prices
                WHERE timestamp between ? AND ?
                GROUP BY ticker_id
            ) earliest
            ON p.ticker_id = earliest.ticker
            AND p.timestamp = earliest.max_ts
            ORDER BY p.ticker_id
        ),
        last_price AS (
            SELECT p.ticker_id as ticker, p.close AS last_close, p.timestamp
            FROM prices p
            JOIN (
                SELECT ticker_id as ticker, MAX(timestamp) AS max_ts
                FROM prices
                WHERE timestamp between ? AND ?
                GROUP BY ticker_id
            ) latest
            ON p.ticker_id = latest.ticker
            AND p.timestamp = latest.max_ts
            ORDER BY p.ticker_id
        )
        SELECT ((lp.last_close - fp.last_close) / fp.last_close) * 100 AS percent_change,
               fp.ticker
        FROM first_price fp
        JOIN last_price lp ON fp.ticker = lp.ticker
        ORDER BY percent_change DESC
        LIMIT ?

    """

    cursor.execute(query_sql, (start_time, day_after_first, end_time, day_after_last, n))
    top_performers = cursor.fetchall()
    conn.close()
    return top_performers


def get_first_and_last_trade_price(db_path: str):
    """
        Find the first and last trade price for each ticker per day.
    """
    print("Retrieving first and last trade prices...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query_sql = """
        WITH bounds AS (
            SELECT 
                ticker_id,
                MIN(timestamp) AS min_ts,
                MAX(timestamp) AS max_ts
            FROM prices
            GROUP BY ticker_id, DATE(timestamp)
        )
        SELECT p.ticker_id AS ticker,
            p.close,
            p.timestamp
        FROM prices p
        JOIN bounds b 
        ON p.ticker_id = b.ticker_id
        AND (p.timestamp = b.min_ts OR p.timestamp = b.max_ts)
        ORDER BY p.ticker_id, p.timestamp;
    """

    cursor.execute(query_sql)
    prices = cursor.fetchall()
    
    conn.close()
    return prices


if __name__ == "__main__":
    db_path = 'market_data.db'
    main_table = "prices" 

    # Initialize the database schema
    print("Checking database schema...")

    if not table_exists(db_path, main_table):
        print("Table not found. Initializing schema...")
        create_schema(db_path)
        print("Schema created.")
    else:
        print("Schema already initialized. Skipping.")

    # load tickers data and insert into the database
    print("Inserting tickers data...")
    tickers_data = load_ticker_data()
    #insert_tickers_data(db_path, tickers_data.values.tolist())
    print("Tickers data inserted successfully.")

    # load market data and insert into the database
    print("Inserting market data...")
    market_data = load_market_data(tickers_data['symbol'].unique().tolist())
    #insert_market_data(db_path, market_data.values.tolist())
    print("Market data inserted successfully.")

    # Retrieve sample data
    d = retrieve_market_data(db_path, 'AAPL', '2025-11-11', '2025-11-20')
    print(d[:5])  # print first 5 rows

    # Calculate average daily volume
    avg_volume = calc_avg_daily_volume(db_path)
    print(f"Average Daily Volume: {avg_volume}")

    # Get top performers
    top_performers = get_top_performers(db_path, n=3, start_time='2025-11-17', end_time='2025-11-21')
    print(f"Top Performers: {top_performers}")

    # Get first and last trade price
    first_last_prices = get_first_and_last_trade_price(db_path)
    print(f"First and Last prices: {first_last_prices}")
