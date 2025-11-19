import yfinance as yf
import pandas as pd
import ccxt 
import time
from config import *



def get_data_eq(ticker: str, start, end, interval: str = "1m") -> pd.DataFrame:
    # get data from yfinance

    data = yf.download(ticker, start=start, end=end, interval=interval)
    data = data.reset_index()
    
    # If multi-index columns, flatten them by taking only the first level
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    data['Symbol'] = ticker
    
    return data


def get_ccxt_ohlcv(exchange_id, symbol, timeframe, start, end):
    # get data from coinbase via ccxt

    ex_class = getattr(ccxt, exchange_id)
    exchange = ex_class()

    start_ms = int(pd.Timestamp(start, tz='UTC').timestamp() * 1000)
    end_ms   = int(pd.Timestamp(end,   tz='UTC').timestamp() * 1000)

    all_rows = []
    since = start_ms
    limit = 500

    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        if not ohlcv:
            break

        all_rows.extend(ohlcv)
        last_ts = ohlcv[-1][0]
        since = last_ts + 1

        if last_ts >= end_ms:
            break

        time.sleep(exchange.rateLimit / 1000)

    if not all_rows:
        return pd.DataFrame(columns=["Datetime", "Open", "High", "Low", "Close", "Volume"])

    df = pd.DataFrame(all_rows, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
    df["Datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    df = df[(df["Datetime"] >= pd.Timestamp(start, tz='UTC')) &
            (df["Datetime"] <= pd.Timestamp(end,   tz='UTC'))]

    df = df.reset_index().drop(columns=["index"])
    df['Symbol'] = symbol
    return df[["Datetime", "Open", "High", "Low", "Close", "Volume", "Symbol"]]


def preprocess_data(df: pd.DataFrame, window: int = 12) -> pd.DataFrame:
    df.dropna(inplace=True)
    df.set_index('Datetime', inplace=True)
    df.sort_index(inplace=True)

    df['returns'] = df['Close'].pct_change().fillna(0)
    df['ma'] = df['Close'].rolling(window=window).mean().fillna(method='bfill')
    
    return df


if __name__ == "__main__":
    # load and save sample data
    st = "2025-11-18"
    et = "2025-11-19"

    eq_data = get_data_eq("AAPL", start=st, end=et, interval="1m")
    print(eq_data.head())
    eq_data.to_csv(data_path + "AAPL_1m.csv", index=False)

    crpyto_data = get_ccxt_ohlcv(
        exchange_id=coinbase_exchange_id,
        symbol="BTC/USD",
        timeframe="1m",
        start=st,
        end=et
    )
    print(crpyto_data.head())
    crpyto_data.to_csv(data_path + "BTCUSD_1m.csv", index=False)

    #process data
    eq_data_processed = preprocess_data(eq_data, window=12)
    print(eq_data_processed.head())
    crpyto_data_processed = preprocess_data(crpyto_data, window=12)
    print(crpyto_data_processed.head())



