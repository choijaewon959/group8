# Assignment 11: Machine Learning in Financial Forecasting and Strategy

This assignment implements a signal generation and backtesting pipeline for financial time series analysis and Machine Learning.

## Overview

The system generates trading signals through feature engineering and evaluates their performance via backtesting. The workflow consists of 4 main components:

1. **Feature Engineering**: Preprocess the features
2. **Model Training**: Train the models that are used to generate the trading signals
3. **Signal Generator**: Creates trading signals from market data using technical indicators and machine learning features
4. **Backtester**: Evaluates signal performance and generates comprehensive results

## Usage

### 1. Generate Signals
```bash
python signal_generator.py
```
This processes market data and generates trading signals with associated features.

### 2. Run Backtesting
```bash
python backtest.py
```
This evaluates the generated signals and saves performance metrics and results.

## Components

- `signal_generator.py` - Main signal generation pipeline
- `backtest.py` - Backtesting engine and performance evaluation
- `feature_engineering.py` - Technical indicator calculations and feature creation
- `tests/` - Unit tests for feature engineering validation

## Output

All results are automatically saved to the appropriate output directories during the backtesting process, including:
- Signal performance metrics
- Trade analysis
- Feature importance scores
- Backtesting summary reports

## Testing

Run the test suite to validate feature engineering and train/test models:
```bash
pytest tests/
```
