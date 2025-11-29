# Format Comparison: SQLite3 vs Parquet

This document compares SQLite3 and Parquet as storage formats for multi-ticker OHLCV market data. The evaluation is based on file size, query performance, workflow integration, and use cases within trading systems.

---

## 1. Storage Size

| Storage Format | File Size |
|----------------|-----------|
| SQLite Database (.db) | 0.69 MB |
| Parquet Dataset (partitioned by ticker) | 0.30 MB |

Parquet provides better storage efficiency due to columnar compression, while SQLite stores complete rows, resulting in a larger file size.

---

## 2. Query Performance

The following benchmark was conducted using a representative query:  
Retrieve TSLA data between 2025-11-17 and 2025-11-18.

| Engine | Query Time |
|--------|------------|
| SQLite3 | 0.002003 sec |
| Parquet | 0.003932 sec |

SQLite returns results faster for small-range lookups because it is row-oriented and operates from a single local database file.  
Parquet introduces file-system and filtering overhead but performs well when scanning large datasets.

A second workload, 5-day rolling volatility for all tickers, shows the opposite trend.  
Parquet handles analytical tasks efficiently since it loads only required columns and benefits from columnar layout.

---

## 3. Integration With Analytics Workflows

### SQLite3
- Simple SQL interface.  
- Useful for small to medium datasets.  
- Convenient for repeated point lookups in event-driven backtesting.  
- Limited scalability and not optimized for large batch analytics.

### Parquet
- Native support in pandas, PyArrow, Spark, and other analytical tools.  
- Efficient for rolling computations, factor analysis, and cross-sectional studies.  
- Scales well with large historical datasets.  
- Less suitable for ad-hoc SQL queries unless paired with tools like DuckDB.

---

## 4. Use Case Analysis

### 4.1 SQLite3 in Trading Systems
SQLite is effective when:
- Backtests require frequent retrieval of short time windows.
- Portability of a single database file is desirable.
- Storage size is not the primary constraint.
- The system is running on a single machine.

SQLite is not ideal for large datasets or workloads requiring parallelism.

### 4.2 Parquet in Trading Systems
Parquet is effective when:
- Working with large historical datasets.
- Performing analytics such as rolling windows, factor modeling, or ML feature generation.
- Integrating with cloud or distributed systems (e.g., Spark, S3).
- Storage efficiency matters.

Parquet is not designed for real-time querying or low-latency execution layers.

---

## 4.3 Support for Backtesting, Live Trading, and Research

### Backtesting
- SQLite is well suited because backtests involve frequent small-range lookups.
- Parquet can be used for preprocessing inputs but is slower for random access during simulation.

### Live Trading
- SQLite can support configurations or static reference data.
- Parquet is generally unsuitable due to access latency and file-based architecture.

### Research and Analytics
- Parquet is preferred for large-scale analysis, machine learning pipelines, and feature engineering.
- SQLite is sufficient for smaller research
