import yfinance as yf
import pandas as pd

def load_data_eq(ticker: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    Load historical market data for a given ticker symbol.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The period over which to fetch data (default is "1mo").
        interval (str): The data interval (default is "1d").

    Returns:
        pd.DataFrame: DataFrame containing historical market data.
    """
    data = yf.download(ticker, period=period, interval=interval)
    return data

def load_data_crypto(ticker: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    Load historical market data for a given cryptocurrency ticker symbol.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., "BTC-USD").
        period (str): The period over which to fetch data (default is "1mo").
        interval (str): The data interval (default is "1d").

    Returns:
        pd.DataFrame: DataFrame containing historical market data.
    """
    data = yf.download(ticker, period=period, interval=interval)
    return data


if __name__ == "__main__":
    # Example usage
    eq_data = load_data_eq("AAPL", period="3mo", interval="1d")
    print("Equity Data:")
    print(eq_data.head())

    # crypto_data = load_data_crypto("BTC-USD", period="3mo", interval="1d")
    # print("\nCryptocurrency Data:")
    # print(crypto_data.head())