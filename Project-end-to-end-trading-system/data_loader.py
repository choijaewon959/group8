import yfinance as yf
import pandas as pd
import ccxt 
import time
from config import *



def load_data_eq(ticker: str, period: str = "1mo", interval: str = "1m") -> pd.DataFrame:
    data = yf.download(ticker, period=period, interval=interval)
    return data


def get_ccxt_ohlcv(exchange_id, symbol, timeframe, start, end):
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

    return df[["Datetime", "Open", "High", "Low", "Close", "Volume"]]



if __name__ == "__main__":
    eq_data = load_data_eq("AAPL", period="3mo", interval="1d")
    print("Equity Data:")
    print(eq_data.head())

    # Example: BTC/USD on Kraken
    crpyto_data = get_ccxt_ohlcv(
        exchange_id=coinbase_exchange_id,
        symbol="BTC/USD",
        timeframe="1m",
        start="2025-11-18",
        end="2025-11-19"
    )
    print(crpyto_data.head())
