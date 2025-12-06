import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import json

def load_signals(signals_path="data/signals_output.csv"):
    df = pd.read_csv(signals_path)
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    return df

def compute_returns(df):
    # generate return_1d
    df["close_next"] = df.groupby("ticker")["close"].shift(-1)
    df["return_1d"] = (df["close_next"] - df["close"]) / df["close"]
    df["return_1d"] = df["return_1d"].fillna(0)
    return df

def backtest_strategy(df, signal_col="signal"):
    # signal base backtest
    df["position"] = df[signal_col].shift(1).fillna(0)  
    df["strategy_return"] = df["position"] * df["return_1d"]

    df["equity_curve"] = (1 + df["strategy_return"]).cumprod()
    df["buy_hold_curve"] = (1 + df["return_1d"]).cumprod()

    return df

def plot_equity_curve(df, output_path="data/backtest_plot.png"):
    # save equity curve as png
    plt.figure(figsize=(10, 6))
    plt.plot(df["equity_curve"], label="Strategy")
    plt.plot(df["buy_hold_curve"], label="Buy & Hold", linestyle="--")
    plt.title("Backtest: Strategy vs Buy & Hold")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    print(f"[Saved] Equity curve → {output_path}")

def plot_confusion_matrix(df, output_path="data/confusion_matrix.png"):
    """signal vs actual movement confusion matrix"""
    # Actual next-day movement
    actual = np.where(df["return_1d"] > 0, 1, 0)
    predicted = np.where(df["signal"] > 0, 1, 0)  # 1 = long, 0 = flat/short
    
    cm = confusion_matrix(actual, predicted)
    disp = ConfusionMatrixDisplay(cm, display_labels=["Down", "Up"])
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix: Signal vs Next-Day Direction")
    plt.savefig(output_path)
    plt.close()
    print(f"[Saved] Confusion matrix → {output_path}")

def plot_feature_importance(model_path="data/best_model.json", 
                            output_path="data/feature_importance.png"):
    """RandomForest feature importance plot"""
    try:
        with open(model_path, "r") as f:
            model_info = json.load(f)

        if model_info["best_model"] != "RandomForestClassifier":
            print("RandomForest not used → skipping feature importance.")
            return

        import joblib
        model = joblib.load("data/best_model.pkl")

        features = model_info["feature_cols"]
        importances = model.feature_importances_

        plt.figure(figsize=(8, 10))
        plt.barh(features, importances)
        plt.title("Feature Importance (Random Forest)")
        plt.xlabel("Importance")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print(f"[Saved] Feature importance → {output_path}")

    except Exception as e:
        print(f"Feature importance skipped (error: {e})")

def main():
    df = load_signals()
    df = compute_returns(df)
    df = backtest_strategy(df)
    df.to_csv("data/backtest_results.csv", index=False)
    print("Backtest results saved → data/backtest_results.csv")

    plot_equity_curve(df)
    plot_confusion_matrix(df)
    plot_feature_importance()

    return df

if __name__ == "__main__":
    main()
