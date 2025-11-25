import sqlite3
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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO tickers (ticker_id, symbol, name, exchange)
        VALUES (?, ?, ?, ?)
    """

    cursor.executemany(insert_sql, data)
    
    conn.commit()
    conn.close()


def insert_market_data(db_path: str, data: list):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO prices (timestamp, ticker_id, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.executemany(insert_sql, data)
    
    conn.commit()
    conn.close()




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
    insert_tickers_data(db_path, tickers_data.values.tolist())
    print("Tickers data inserted successfully.")

    # load market data and insert into the database
    print("Inserting market data...")
    market_data = load_market_data(tickers_data['symbol'].unique().tolist())
    insert_market_data(db_path, market_data.values.tolist())
    print("Market data inserted successfully.")

