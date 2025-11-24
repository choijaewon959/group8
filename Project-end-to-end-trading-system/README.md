# Trading System

End-to-end trading system with backtesting and live trading capabilities.

## Overview

This system supports:
- **Backtesting**: Test strategies on historical data
- **Live Trading**: Execute strategies with Alpaca API using real-time crypto data

## Quick Start

### 1. Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Create `.env` file with your Alpaca credentials:
```
ALPACA_API_KEY=your_api_key
ALPACA_SECRET_KEY=your_secret_key
```

### 2. Backtesting

Run the backtester:
```bash
python engine_run.py
```

View performance analysis:
```bash
jupyter notebook performance_report.ipynb
```

### 3. Live Trading

Run live trading with Alpaca:
```bash
python main.py
```

**Note**: 
1. Live trading uses CCXT for real-time crypto market data (BTC/USD) and Alpaca for order execution.
2. All the backtesting data intervals are based on 1 min interval. To leverage the same interval trading strategy, bar_builder class has been introduced to simulate minute interval ticker.


## Project Structure

```
.
├── engine_run.py              # Backtesting engine entry point
├── main.py                    # Live trading entry point
├── performance_report.ipynb   # Performance analysis notebook
├── data_loader.py             # Data fetching (yfinance, CCXT, Alpaca)
├── bar_builder.py             # Real-time OHLC bar construction (real-time to 1min bar)
├── config.py                  # Configuration settings
├── strategy/                  # Trading strategies
│   ├── ma_cross.py           # Moving average crossover
│   ├── momentum.py           # Momentum strategy
│   └── strategybase.py       # Base strategy class
├── data/                      # Historical data storage
└── result/                    # Backtest results
```

## Data Sources

- **Historical Stock Data**: yfinance
- **Historical Crypto Data**: CCXT (Coinbase)
- **Live Crypto Data**: CCXT Pro (streaming)
- **Alpaca**: Order execution (paper trading)

## Strategies

### Moving Average Crossover
- Short MA vs Long MA signals
- Configurable windows (default: 20/60)

### Momentum
- Price momentum-based entries
- Configurable lookback period

## Requirements

- Python 3.13+
- Alpaca paper trading account
- Internet connection for live data feeds
