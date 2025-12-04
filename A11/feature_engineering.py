import pandas as pd
import numpy as np


data_dir_path = './data/'
market_data_path = data_dir_path + 'market_data_ml.csv'
tickers_data_path = data_dir_path + 'tickers-1.csv'

config_dir_path = './config/'
features_config_path = config_dir_path + 'features_config.json'


def load_data() -> tuple[pd.Series, pd.DataFrame]:
    tickers = pd.read_csv(tickers_data_path)['symbol']
    df_data = pd.read_csv(market_data_path)

    return tickers, df_data


def add_zscore(df, col, window=60):
    mean = df[col].rolling(window).mean()
    std = df[col].rolling(window).std()
    df[col + '_z'] = (df[col] - mean) / std
    return df


def preprocess_data(df: pd.DataFrame, normalize=True, z_window=60) -> pd.DataFrame:
    feature_cfg = pd.read_json(features_config_path)
    features = feature_cfg['features']
    label = feature_cfg['label'].iloc[0]
    
    df = df[['date', 'ticker', 'close']].copy()
    df = df.sort_values(by='date').reset_index(drop=True)

    # generate label
    if label == 'direction':
        df[label] = (df['close'].shift(-1) > df['close']).astype(int)

    # generate features
    for f in features:
        if f == 'return_1d':
            df[f] = df['close'].pct_change().fillna(0)
            df[f + '_log'] = np.log1p(df[f])
            df = add_zscore(df, f, z_window)
            df = add_zscore(df, f + '_log', z_window)

        if f == 'return_3d':
            df[f] = df['close'].pct_change(3).fillna(0)
            df[f + '_log'] = np.log1p(df[f])
            df = add_zscore(df, f, z_window)
            df = add_zscore(df, f + '_log', z_window)

        if f == 'return_5d':
            df[f] = df['close'].pct_change(5).fillna(0)
            df[f + '_log'] = np.log1p(df[f])
            df = add_zscore(df, f, z_window)
            df = add_zscore(df, f + '_log', z_window)

        if f == 'sma_5':
            df[f] = df['close'].rolling(5).mean().bfill()
            if normalize:
                dev_col = f + '_dev'
                df[dev_col] = (df['close'] - df[f]) / df[f]
                df = add_zscore(df, dev_col, z_window)

        if f == 'sma_10':
            df[f] = df['close'].rolling(10).mean().bfill()
            if normalize:
                dev_col = f + '_dev'
                df[dev_col] = (df['close'] - df[f]) / df[f]
                df = add_zscore(df, dev_col, z_window)

        if f == 'rsi_14':
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            df[f] = 100 - (100 / (1 + rs))
            df[f] = df[f].fillna(0)
            df = add_zscore(df, f, z_window)

        if f == 'macd':
            ema12 = df['close'].ewm(span=12, adjust=False).mean()
            ema26 = df['close'].ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            df[f] = macd

            if normalize:
                norm_col = f + '_norm'
                df[norm_col] = macd / ema26
                df = add_zscore(df, norm_col, z_window)

    return df


if __name__ == "__main__":
    # 1. load data
    df_ticker, df_data = load_data()
    
    # 2. preprocess data for each ticker
    data_list = []
    for tckr in df_ticker:
        df_ticker_data = df_data[df_data['ticker'] == tckr]
        df_ticker_data_preprocessed = preprocess_data(df_ticker_data)
        data_list.append(df_ticker_data_preprocessed)

    # 3. combine all ticker data
    df_all = pd.concat(data_list, ignore_index=True)
    print(df_all.head())