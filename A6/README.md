# A6: Design Patterns in Financial Analytics

## Overview
This project demonstrates the implementation of various design patterns in a financial analytics system. It includes trading strategies, portfolio management, and real-time market data analysis using object-oriented design principles.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd group8/A6
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install numpy matplotlib memory-profiler pytest pandas
   ```

3. **Run the main application**:
   ```bash
   python main.py
   ```

4. **Run tests** (from project root):
   ```bash
   cd ..
   pytest
   ```

## Module Descriptions

### Core Modules

#### `main.py`
- **Purpose**: Entry point for the application
- **Functionality**: Orchestrates the execution of trading strategies, analytics, and pattern demonstrations
- **Usage**: Run `python main.py` to execute the full pipeline

#### `models.py`
- **Purpose**: Core data models and structures
- **Contains**: 
  - Market data point classes
  - Portfolio structures
  - Financial instrument definitions
- **Design Patterns**: Data Transfer Object (DTO) pattern

#### `data_loader.py`
- **Purpose**: Data loading and preprocessing utilities
- **Functionality**: Loads market data from CSV files and external sources
- **Features**: Data validation and cleaning

#### `analytics.py`
- **Purpose**: Financial analytics and calculations
- **Contains**:
  - Portfolio performance metrics
  - Risk calculations
  - Statistical analysis functions

### Strategy Framework

#### `engine.py`
- **Purpose**: Strategy execution engine
- **Functionality**: Orchestrates strategy execution and portfolio updates
- **Design Patterns**: Template Method Pattern

#### `invokers.py`
- **Purpose**: Command invoker implementations
- **Functionality**: Manages command execution and queuing
- **Features**: Batch processing and transaction management

### Design Pattern Implementations

#### `patterns/factory_pattern.py`
- **Purpose**: Factory pattern implementation for creating financial instruments
- **Functionality**: 
  - Creates different types of assets (stocks, bonds, derivatives)
  - Centralizes object creation logic
- **Benefits**: Loose coupling and easy extensibility

#### `patterns/builder_pattern.py`
- **Purpose**: Builder pattern for complex portfolio construction
- **Functionality**:
  - Step-by-step portfolio building
  - Validation at each construction step
- **Benefits**: Clear construction process and immutable results

#### `patterns/strategy_pattern.py`
- **Purpose**: Strategy pattern implementation for trading algorithms
- **Design Patterns**: Strategy Pattern
- **Functionality**:
  - Moving average strategies
  - Mean reversion strategies
  - Momentum strategies
- **Benefits**: Pluggable strategy interface for easy extension

#### `patterns/command_pattern.py`
- **Purpose**: Command pattern implementation
- **Design Patterns**: Command Pattern
- **Functionality**:
  - Encapsulates trading operations as command objects
  - Supports undo/redo operations
  - Transaction logging
- **Benefits**: Decoupled execution and flexible operation management

#### `patterns/observer_pattern.py`
- **Purpose**: Observer pattern for event-driven updates
- **Design Patterns**: Observer Pattern
- **Functionality**:
  - Real-time portfolio value updates
  - Market event notifications
  - Performance monitoring
- **Benefits**: Loose coupling between event sources and handlers

### Configuration

#### `config/config.py`
- **Purpose**: Configuration management
- **Contains**: Application settings and parameters

#### `config/config.json`
- **Purpose**: JSON configuration file
- **Contains**: Runtime parameters and feature flags

#### `config/strategy_params.json`
- **Purpose**: Strategy-specific parameters
- **Contains**: Window sizes, thresholds, and strategy configurations

#### `config/portfolio_structure.json`
- **Purpose**: Portfolio composition settings
- **Contains**: Asset allocation and risk parameters

### Testing

#### `tests/`
- **Purpose**: Unit and integration tests
- **Coverage**: All major modules and design patterns
- **Framework**: pytest
- **Run**: `pytest` from project root

## Design Patterns Demonstrated

1. **Strategy Pattern**: Interchangeable trading algorithms (`patterns/strategy_pattern.py`)
2. **Factory Pattern**: Financial instrument creation (`patterns/factory_pattern.py`)
3. **Builder Pattern**: Complex portfolio construction (`patterns/builder_pattern.py`)
4. **Command Pattern**: Trade execution with undo capability (`patterns/command_pattern.py`)
5. **Observer Pattern**: Real-time event notifications (`patterns/observer_pattern.py`)
6. **Template Method**: Strategy execution framework (`engine.py`)

## Usage Examples

### Basic Strategy Execution
```python
from patterns.strategy_pattern import MovingAverageStrategy
from engine import ExecutionEngine

strategy = MovingAverageStrategy(window=20)
engine = ExecutionEngine()
engine.generate_all_signals(strategy, symbol)
```

### Portfolio Building
```python
from patterns.builder_pattern import PortfolioBuilder

portfolio = (PortfolioBuilder()
    .add_stock("AAPL", 100)
    .add_bond("US10Y", 50)
    .set_cash(10000)
    .build())
```

### Command Execution
```python
from patterns.command_pattern import BuyCommand
from invokers import TradeInvoker

buy_cmd = BuyCommand("AAPL", 100)
invoker = TradeInvoker()
invoker.execute(buy_cmd)
```

### Observer Pattern Usage
```python
from patterns.observer_pattern import PortfolioObserver, MarketEventSubject

observer = PortfolioObserver()
subject = MarketEventSubject()
subject.attach(observer)
```

## Data Requirements

- Market data in CSV format in the `data/` directory
- Supported columns: timestamp, symbol, price, volume
- Configuration files in `config/` directory

## Contributing

1. Follow existing code structure and naming conventions
2. Add tests for new functionality
3. Update this README for new modules or patterns
4. Ensure all tests pass before submitting

## Authors
- Group 8, FINM325 - University of Chicago

---
For detailed implementation examples and advanced usage, refer to the source code and test files.
