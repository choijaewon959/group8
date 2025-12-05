import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from feature_engineering import load_data, preprocess_data

def load_config(features_path: str, params_path: str):
    with open(features_path, "r") as f:
        features_cfg = json.load(f)
    with open(params_path, "r") as f:
        params_cfg = json.load(f)
    return features_cfg, params_cfg


def prepare_data(df: pd.DataFrame, features_cfg: dict):
    all_train_cols = features_cfg["features_train"]
    label_col = features_cfg["label"]

    non_feature_cols = {"date", "ticker", "close", label_col}
    feature_cols = [c for c in all_train_cols if c not in non_feature_cols]

    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    df = df[["date", "ticker"] + feature_cols + [label_col]].dropna()

    X = df[feature_cols].values
    y = df[label_col].values

    return X, y, feature_cols, df


def build_models(model_params: dict):
    models = {}

    if "LogisticRegression" in model_params:
        params = model_params["LogisticRegression"]
        models["LogisticRegression"] = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(**params))
        ])

    if "RandomForestClassifier" in model_params:
        params = model_params["RandomForestClassifier"]
        models["RandomForestClassifier"] = RandomForestClassifier(
            **params, random_state=42
        )

    return models

def time_series_split(X, y, split_ratio=0.8):
    split = int(len(X) * split_ratio)
    return X[:split], X[split:], y[:split], y[split:]

def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return acc, report

def train_models(models, X_train, y_train, X_test, y_test):
    results = {}

    for name, model in models.items():
        print(f"Training {name} ===")
        model.fit(X_train, y_train)
        acc, report = evaluate(model, X_test, y_test)

        print(f"{name} Accuracy: {acc}")
        print(report)

        results[name] = {
            "model": model,
            "accuracy": acc,
            "report": report
        }

    return results

def main(
    features_cfg_path="config/features_config.json",
    params_cfg_path="config/model_params.json"
):
    df_ticker, df_data = load_data()

    data_list = []
    for tckr in df_ticker:
        df_ticker_data = df_data[df_data['ticker'] == tckr]
        df_ticker_data_preprocessed = preprocess_data(df_ticker_data)
        data_list.append(df_ticker_data_preprocessed)

    df = pd.concat(data_list, ignore_index=True)

    features_cfg, model_params = load_config(features_cfg_path, params_cfg_path)

    X, y, feature_cols, df_trimmed = prepare_data(df, features_cfg)

    X_train, X_test, y_train, y_test = time_series_split(X, y)

    models = build_models(model_params)

    results = train_models(models, X_train, y_train, X_test, y_test)

    best = max(results, key=lambda m: results[m]["accuracy"])
    print(f"BEST MODEL: {best} (acc={results[best]['accuracy']})")

    return results


if __name__ == "__main__":
    main()