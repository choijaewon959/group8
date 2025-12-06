import json
import pandas as pd
import numpy as np

from train_model import main as train_model_main
from feature_engineering import load_data, preprocess_data


def prepare_feature_data(df, features_cfg):
    """using, train_model.py prepare_data()"""

    all_train_cols = features_cfg["features_train"]
    label_col = features_cfg["label"]

    non_feature_cols = {"date", "ticker", "close", label_col}
    feature_cols = [c for c in all_train_cols if c not in non_feature_cols]

    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    df = df[["date", "ticker", "close"] + feature_cols + [label_col]]

    df = df.dropna()

    X = df[feature_cols].values
    return df, X, feature_cols


def generate_signal(prob, upper=0.55, lower=0.45):
    if prob > upper:
        return 1
    elif prob < lower:
        return -1
    return 0


def main(features_cfg_path="config/features_config.json"):

    # 1) model train
    results = train_model_main()
    best_name = max(results, key=lambda m: results[m]["accuracy"])
    model = results[best_name]["model"]

    # 2) feature engineering
    tickers, raw = load_data()
    dfs = [preprocess_data(raw[raw["ticker"] == t]) for t in tickers]
    df_all = pd.concat(dfs, ignore_index=True)

    # 3) feature trimming
    with open(features_cfg_path, "r") as f:
        features_cfg = json.load(f)

    df_trim, X, feature_cols = prepare_feature_data(df_all, features_cfg)

    # 4) forecast
    prob = model.predict_proba(X)[:, 1]
    df_trim["proba"] = prob
    df_trim["signal"] = [generate_signal(p) for p in prob]

    # 5) save result
    df_trim.to_csv("./data/signals_output.csv", index=False)
    print("Saved signals to ./data/signals_output.csv")

    return df_trim


if __name__ == "__main__":
    main()
