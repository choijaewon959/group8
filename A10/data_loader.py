import numpy as np
import pandas as pd


market_data_path = './market_data/market_data_multi.csv'
tickers_data_path = './market_data/tickers.csv'


def validate_tickers(func):
    def wrapper(tickers, *args, **kwargs):
        df_data = func(*args, **kwargs)
        valid_tickers = set(tickers)

        for ticker in valid_tickers:
            if ticker not in df_data['ticker'].unique():
                raise ValueError(f"Ticker {ticker} from tickers.csv not found in market data.")
            
        return df_data
    return wrapper


@validate_tickers
def load_market_data():
    df = pd.read_csv(market_data_path)

    # Convert timestamp to datetime
    if np.issubdtype(df['timestamp'].dtype, np.number):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC')

    # drop rows with missing values
    df = df.dropna(subset=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    return df


def load_ticker_data():
    df_tickers = pd.read_csv(tickers_data_path)
    return df_tickers


if __name__ == "__main__":
    try:
        data_tickers= load_ticker_data()
        tickers = data_tickers['symbol'].unique().tolist()
        data = load_market_data(tickers)
        print(data.head())
    except ValueError as e:
        print(f"Validation error: {e}")