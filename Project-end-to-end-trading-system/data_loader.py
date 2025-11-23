import yfinance as yf
import pandas as pd
import ccxt 
import time
import os
from config import *
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def get_data_eq(ticker: str, start, end, interval: str = "1m") -> pd.DataFrame:
    # get data from yfinance with extended hours (premarket + regular + aftermarket)

    data = yf.download(ticker, start=start, end=end, interval=interval, prepost=True)
    data = data.reset_index()
    
    # If multi-index columns, flatten them by taking only the first level
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Map to Alpaca-compatible column names
    column_mapping = {
        'Datetime': 'timestamp',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }
    data = data.rename(columns=column_mapping)
    
    # Ensure timestamp is timezone-aware UTC (matching Alpaca format)
    if data['timestamp'].dt.tz is None:
        data['timestamp'] = pd.to_datetime(data['timestamp']).dt.tz_localize('UTC')
    else:
        data['timestamp'] = pd.to_datetime(data['timestamp']).dt.tz_convert('UTC')
    
    data['symbol'] = ticker
    
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
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "symbol"])

    df = pd.DataFrame(all_rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    df = df[(df["timestamp"] >= pd.Timestamp(start, tz='UTC')) &
            (df["timestamp"] <= pd.Timestamp(end,   tz='UTC'))]

    df = df.reset_index(drop=True)
    df['symbol'] = symbol
    return df[["timestamp", "open", "high", "low", "close", "volume", "symbol"]]


def convert_alpaca_tf(tf_str):
    tf_str = tf_str.lower()

    if tf_str.endswith("m"):   # minutes
        n = int(tf_str.replace("m", ""))
        return TimeFrame(n, TimeFrameUnit.Minute)

    elif tf_str.endswith("h"): # hours
        n = int(tf_str.replace("h", ""))
        return TimeFrame(n, TimeFrameUnit.Hour)

    elif tf_str.endswith("d"): # days
        n = int(tf_str.replace("d", ""))
        return TimeFrame(n, TimeFrameUnit.Day)

    else:
        raise ValueError(f"Unsupported timeframe: {tf_str}")


def get_data_from_alpaca(symbol: str, start, end, timeframe: str = "1m") -> pd.DataFrame:
    data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        start=start,
        end=end,
        timeframe=convert_alpaca_tf(timeframe),
    )

    bars = data_client.get_stock_bars(request_params)
    df = bars.df
    df = df.reset_index()
    
    # Ensure timestamp is UTC timezone-aware
    if df['timestamp'].dt.tz is None:
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC')
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert('UTC')
    
    # Filter to match yfinance extended hours (4 AM - 8 PM EST = 09:00 - 01:00 UTC next day)
    # This excludes overnight session data from previous day
    df = df[df['timestamp'].dt.hour >= 9].copy()

    return df


def preprocess_data(df: pd.DataFrame, window: int = 12) -> pd.DataFrame:
    df.dropna(inplace=True)
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    
    df['returns'] = df['close'].pct_change().fillna(0)
    df['ma'] = df['close'].rolling(window=window).mean().bfill()
    
    return df



if __name__ == "__main__":
    # load and save sample data

    # query params
    symbol = "AAPL"
    st = "2025-11-18"
    et = "2025-11-19"
    timeframe = "1m"

    # yfinance
    eq_data = get_data_eq(symbol, start=st, end=et, interval=timeframe)
    eq_data.to_csv(data_path + f"{symbol}_{timeframe}.csv", index=False)

    # ccxt - coinbase
    # crpyto_data = get_ccxt_ohlcv(
    #     exchange_id=coinbase_exchange_id,
    #     symbol="BTC/USD",
    #     timeframe="1m",
    #     start=st,
    #     end=et
    # )
    # crpyto_data.to_csv(data_path + "BTCUSD_1m.csv", index=False)

    # alpaca
    al_eq_data = get_data_from_alpaca(symbol, st, et, timeframe)
    al_eq_data.to_csv(data_path + f"AL_{symbol}_{timeframe}.csv", index=False)

    #process data
    # eq_data_processed = preprocess_data(eq_data, window=12)
    # print(eq_data_processed.head())
    # crpyto_data_processed = preprocess_data(crpyto_data, window=12)
    # print(crpyto_data_processed.head())
    al_eq_data_processed = preprocess_data(al_eq_data, window=12)
    print(al_eq_data_processed.head())




