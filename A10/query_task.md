# A10 — Query Tasks Report (SQLite3 & Parquet)

---

# 1. SQLite3 Query Results

## 1.1 TSLA Market Data (Nov 17–18, 2025)

The table below shows 1-minute TSLA market data retrieved from SQLite.

| index | id   | timestamp           | open    | high    | low     | close   | volume |
|------:|------|---------------------|---------|---------|---------|---------|--------|
| 0     | 5866 | 2025-11-17 09:30:00 | 268.31  | 268.51  | 267.95  | 268.07  | 1609   |
| 1     | 5867 | 2025-11-17 09:31:00 | 268.94  | 269.11  | 268.28  | 269.04  | 4809   |
| 2     | 5868 | 2025-11-17 09:32:00 | 267.70  | 267.94  | 267.69  | 267.92  | 1997   |
| 3     | 5869 | 2025-11-17 09:33:00 | 268.45  | 268.64  | 268.00  | 268.56  | 3461   |
| 4     | 5870 | 2025-11-17 09:34:00 | 269.01  | 269.57  | 268.21  | 269.23  | 4003   |

---

## 1.2 AAPL — Average Daily Volume (SQLite)

Average daily volume for AAPL during the selected date range:

```
avg_volume
-----------
4487.50
```

---

## 1.3 Top Performers (SQLite)

Top-return tickers based on computed percentage returns:

| pct_return | ticker |
|-----------:|--------|
| 46.57%     | GOOG   |
| 16.29%     | AAPL   |
| 14.08%     | MSFT   |

---

## 1.4 AAPL — First and Last Trade Prices (SQLite)

| ticker | first_price | first_timestamp       | last_price | last_timestamp        |
|--------|-------------|------------------------|------------|------------------------|
| AAPL   | 270.88      | 2025-11-17 09:30:00    | 287.68     | 2025-11-17 16:00:00    |

---

# 2. Parquet Query Results

## 2.1 AAPL — 5-Minute Resampled OHLCV (Parquet)

| timestamp           | open    | high    | low     | close   | volume |
|---------------------|---------|---------|---------|---------|--------|
| 2025-11-17 09:30:00 | 271.45  | 271.69  | 271.08  | 270.88  | 11019  |
| 2025-11-17 09:35:00 | 270.88  | 271.11  | 270.40  | 270.74  |  6225  |
| 2025-11-17 09:40:00 | 270.74  | 270.89  | 270.01  | 270.28  |  5881  |
| 2025-11-17 09:45:00 | 270.28  | 270.54  | 269.95  | 270.12  |  4332  |
| 2025-11-17 09:50:00 | 270.12  | 270.16  | 269.02  | 269.41  |  8007  |

---

## 2.2 AAPL — Rolling 5-Day Volatility (Parquet)

| timestamp           | close   | return     | vol_5d   |
|---------------------|---------|------------|----------|
| 2025-11-17 09:30:00 | 271.45  | NaN        | NaN      |
| 2025-11-17 09:31:00 | 269.86  | -0.006     | NaN      |
| 2025-11-17 09:32:00 | 271.47  |  0.006     | NaN      |
| 2025-11-17 09:33:00 | 270.05  | -0.005     | NaN      |
| 2025-11-17 09:34:00 | 270.06  |  0.000     | NaN      |

*Volatility requires at least five valid returns before a value can be computed.*

---

## 2.3 Query Time Comparison (SQLite vs Parquet)

| operation                | sqlite_time (s) | parquet_time (s) |
|--------------------------|-----------------|------------------|
| Retrieve TSLA 1-day data | 0.0021          | 0.0044           |

---

## 2.4 File Size Comparison

| format  | size_MB |
|---------|---------|
| SQLite  | 1.20    |
| Parquet | 0.28    |

---

## 2.5 Summary

- SQLite was faster for small-range row queries.
- Parquet files were significantly smaller due to columnar compression.
- Rolling 5-day volatility produces NaN until the window is fully populated.
- Both storage formats support equivalent analytics with differing performance profiles.

