import pandas as pd
import numpy as np
from feature_engineering import preprocess_data, add_zscore


def test_feature_generation():
    test_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10, freq='D'),
        'ticker': 'TEST',
        'close': [100, 101, 102, 101, 103, 102, 104, 105, 104, 106]
    })
    
    result = preprocess_data(test_data.copy())
    
    expected_features = [
        'return_1d', 'return_1d_log', 'return_1d_z', 'return_1d_log_z',
        'sma_5', 'sma_5_dev', 'sma_5_dev_z',
        'rsi_14', 'rsi_14_z'
    ]
    
    for feature in expected_features:
        assert feature in result.columns
    
    expected_return = test_data['close'].pct_change().fillna(0)
    assert result['return_1d'].equals(expected_return)


def test_label_creation():
    test_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10, freq='D'),
        'ticker': 'TEST',
        'close': [100, 101, 102, 101, 103, 102, 104, 105, 104, 106]
    })
    
    result = preprocess_data(test_data.copy())
    
    assert 'direction' in result.columns
    
    unique_labels = result['direction'].dropna().unique()
    assert all(label in [0, 1] for label in unique_labels)


def test_zscore_calculation():
    test_series = pd.DataFrame({'value': [1, 2, 3, 4, 5]})
    result = add_zscore(test_series, 'value', window=5)
    
    assert len(result) == len(test_series)
    
    # Test actual z-score calculation
    # For values [1,2,3,4,5]: mean=3, std=sqrt(2.5)
    expected_zscore = (5 - 3) / np.sqrt(2.5)
    actual_zscore = result.iloc[-1]['value_z']
    assert abs(actual_zscore - expected_zscore) < 0.001


if __name__ == "__main__":
    test_feature_generation()
    test_label_creation()
    test_zscore_calculation()
    print("All tests passed!")