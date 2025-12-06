import os
import pandas as pd
import numpy as np
import pytest

from signal_generator import generate_signal, prepare_feature_data
from signal_generator import main as signal_main
from feature_engineering import preprocess_data
from train_model import main as train_model_main


# ---------------------------
# Test 1: generate_signal()
# ---------------------------

def test_generate_signal():
    assert generate_signal(0.8) == 1      # strong buy
    assert generate_signal(0.2) == -1     # strong sell
    assert generate_signal(0.50) == 0     # hold
    assert generate_signal(0.48) == 0     # inside neutral band


# ---------------------------
# Test 2: feature trimming shape
# ---------------------------

def test_prepare_feature_data_shape():
    # create dummy df similar to preprocess output
    df = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-02"],
        "ticker": ["AAPL", "AAPL"],
        "close": [100, 101],
        "return_1d_z": [0.1, 0.2],
        "return_1d_log_z": [0.1, 0.2],
        "direction": [1, 0]
    })

    features_cfg = {
        "features_train": ["date", "ticker", "close",
                           "return_1d_z", "return_1d_log_z",
                           "direction"],
        "label": "direction"
    }

    df_trim, X, feature_cols = prepare_feature_data(df, features_cfg)

    # check shapes
    assert len(df_trim) == 2
    assert X.shape == (2, 2)  # 2 feature columns (z + log_z)
    assert set(feature_cols) == {"return_1d_z", "return_1d_log_z"}


# ---------------------------
# Test 3: model training returns a model
# ---------------------------

def test_train_model_returns_model():
    results = train_model_main()
    assert isinstance(results, dict)
    best = max(results, key=lambda m: results[m]["accuracy"])
    assert "model" in results[best]


# ---------------------------
# Test 4: Full signal generator flow
# ---------------------------

def test_signal_generator_end_to_end(tmp_path, monkeypatch):
    #Ensure signal_generator creates signals_output.csv

    df_result = signal_main()

    # check dataframe non-empty
    assert len(df_result) > 10

    # check necessary columns exist
    for col in ["proba", "signal", "close"]:
        assert col in df_result.columns

    # check output file created
    assert os.path.exists("data/signals_output.csv") or os.path.exists("signals_output.csv")
