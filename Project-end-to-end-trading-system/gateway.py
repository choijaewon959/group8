import pandas as pd

def get_price_data():
    data = pd.read_csv('./data/market_data.csv')

    market_data_points = [
        (row['Datetime'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
        for _, row in data.iterrows()
    ]

    return market_data_points



