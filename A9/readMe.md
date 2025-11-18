# Assignment 9: Mini Trading System

## Overview

The project builds a simplified electronic trading system.
Four incremental components are implemented:

1	**FIX Message Parser**
<br />2	**Order Lifecycle Simulator**
<br />3	**Risk Check Engine**
<br />4	**Event Logger**

At completion, the system supports this end-to-end event flow:

FIX Message → Parser → Order → RiskEngine → Logger

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd group8/A8
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install pytest numpy"
   ```

3. **Verify installation**:
   ```bash
   python -c "import pytest numpy; print('All dependencies installed successfully')"
   ```

4. **Run the main application**:
   ```bash
   python main.py
   ```

5. **Run tests**:
    Run the following command at root level of A7.
   ```bash
   pytest
   ```

### Core Modules

#### `fix_parser.py`
-Convert incoming FIX protocol strings into validated Python dictionaries:

**Parse key=value FIX fields separated by |**
<br />**Validate required tags (symbol, side, price/qty)**
<br />**Raise ValueError when required data is missing**
<br />**Support multiple FIX message types (orders/quotes/etc.)**


#### `order.py`
-Represent the lifecycle of an order through valid states:

**Maintain strict state transitions**
<br />**If an invalid transition occurs → log or raise error**

#### `risk_engine.py`
-Block orders that violate configured risk limits:

**Validate max order size**
<br />**Maintain and update position limits across symbols**
<br />**Reject risky orders before acknowledgment**

#### `logger.py`
Store and replay important trading events:

**Singleton class**
<br />**JSON-based persistent log (events.json)**
<br />**Log order lifecycle + risk events**

#### `main.py`
-Runs all parts for automated order evaluation from raw FIX messages.

### How to Run

#### Environment
```bash
python3 -m venv venv
<br />source venv/bin/activate
<br />pip install -r requirements.txt
```


### Start the full system
Run the orchestrator:
```bash
python main.py
```

This will launch all core processes sequentially:
<br />**-fix_parser**
<br />**-order**
<br />**-risk_engine**
<br />**-logger**

### Testing
- Run the integrated unit tests:
```bash
pytest -v
```

### Future Extensions

<br />**FIX heartbeat + session management**
<br />**Asynchronous processing using asyncio / ZeroMQ**
<br />**Expand more state transitions (partial fills, modify orders)**
<br />**Add GUI or live feed simulation**
<br />**Integrate quantitative strategy signals**

## Authors
- Group 8, FINM325 - University of Chicago

---

For detailed implementation examples and advanced usage patterns, refer to the source code documentation and the generated performance reports.

