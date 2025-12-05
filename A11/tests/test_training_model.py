import numpy as np
import pandas as pd
from train_model import (
    prepare_data,
    build_models,
    time_series_split,
    train_models,
    evaluate
)

def test_model_training_and_shapes():

    df = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=50),
        "ticker": ["AAPL"] * 50,
        "close": np.random.rand(50) * 100,

        "return_1d_z": np.random.randn(50),
        "return_1d_log_z": np.random.randn(50),
        "return_3d_z": np.random.randn(50),
        "return_3d_log_z": np.random.randn(50),
        "return_5d_z": np.random.randn(50),
        "return_5d_log_z": np.random.randn(50),
        "sma_5_dev": np.random.randn(50),
        "sma_5_dev_z": np.random.randn(50),
        "sma_10_dev": np.random.randn(50),
        "sma_10_dev_z": np.random.randn(50),
        "rsi_14": np.random.randn(50),
        "rsi_14_z": np.random.randn(50),
        "macd_norm": np.random.randn(50),
        "macd_norm_z": np.random.randn(50),

        "direction": np.random.randint(0, 2, size=50)
    })

    #mock feature config
    features_cfg = {
        "features_train": df.columns.tolist(),
        "label": "direction"
    }

    # Mock model params
    model_params = {
        "LogisticRegression": {"C": 1.0, "max_iter": 50},
        "RandomForestClassifier": {"n_estimators": 5, "max_depth": 3},
        "XGBClassifier": {"n_estimators": 5, "learning_rate": 0.1, "max_depth": 2}
    }

    X, y, feature_cols, df_trimmed = prepare_data(df, features_cfg)

    X_train, X_test, y_train, y_test = time_series_split(X, y)

    models = build_models(model_params)

    results = train_models(models, X_train, y_train, X_test, y_test)

    for name, result in results.items():
        model = result["model"]

        # check accuracy computed
        assert isinstance(result["accuracy"], float)

        # Check prediction shape
        y_pred = model.predict(X_test)
        assert y_pred.shape[0] == X_test.shape[0]

        # check predictions are 0 or 1
        assert np.all(np.isin(y_pred, [0, 1]))