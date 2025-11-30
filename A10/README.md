
# Assignment 10 - Data Storage Performance

Comparison of SQLite vs Parquet storage for market data analysis.

## Overview

This assignment explores different data storage formats and their performance characteristics:
- **SQLite**: Relational database with SQL query capabilities
- **Parquet**: Columnar storage format optimized for analytics

## Files

- `sqlite_storage.py` - SQLite database operations
- `parquet_storage.py` - Parquet file operations  
- `data_loader.py` - Market data loading utilities
- `schema.sql` - Database schema definition
- `comparison.md` - Performance comparison results
- `query_tasks.md` / `query_tasks.ipynb` - Query analysis tasks

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize SQLite Database
```bash
python sqlite_storage.py
```

### 3. Generate Parquet Files
```bash
python parquet_storage.py
```

### 4. Run Comparisons
Open `query_tasks.ipynb` to see performance analysis and query comparisons.

## Data Structure

The market data includes:
- Timestamps
- Stock symbols  
- OHLC prices (Open, High, Low, Close)
- Volume

## Storage Formats

**SQLite Benefits:**
- ACID compliance
- Complex relational queries
- Concurrent access
- Built-in indexing

**Parquet Benefits:**  
- Columnar compression
- Fast analytical queries
- Schema evolution
- Cross-platform compatibility