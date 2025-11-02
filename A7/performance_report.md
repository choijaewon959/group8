# Performance Report: Rolling Metrics Parallel Computation

This report summarizes the performance of rolling metrics computation across three symbols(AAPL, MSFT, SPY) using **Pandas** and **Polars**, with both **Threading** and **Multiprocessing** approaches. The goal is to compare **execution time** and **CPU utilization** for different window sizes.


To measure CPU utilization during the execution of the rolling metrics computations, we sampled the CPU usage of the process at 0.5-second intervals using psutil. These periodic readings were then **averaged** to obtain the mean CPU usage over the duration of each computation. This method provides an approximate view of the CPU load while the parallel tasks were running.

---

## 1. Window Size: 30

| Library | Method           | Time (s) | Avg CPU (%) |
|---------|-----------------|-----------|-------------|
| Pandas  | Threading        | 0.06      | 37.2        |
| Pandas  | Multiprocessing  | 3.17      | 5.8         |
| Polars  | Threading        | 0.02      | 232.7       |
| Polars  | Multiprocessing  | 3.26      | 6.3         |

**Observations:**

- Threading is extremely fast for small window sizes.
- Polars shows significantly higher CPU utilization with threading, suggesting it is more parallel internally.
- Multiprocessing overhead dominates for small data chunks, leading to longer times and low CPU usage.

---

## 2. Window Size: 1000

| Library | Method           | Time (s) | Avg CPU (%) |
|---------|-----------------|-----------|-------------|
| Pandas  | Threading        | 0.06      | 116.3       |
| Pandas  | Multiprocessing  | 3.19      | 3.0         |
| Polars  | Threading        | 0.02      | 347.2       |
| Polars  | Multiprocessing  | 3.22      | 4.3         |

**Observations:**

- Increasing the window size barely affects threading times due to efficient vectorized operations.
- Threading CPU usage increases substantially with Polars, showing strong internal parallelism.
- Multiprocessing still suffers from overhead; for small-to-medium workloads, threading is more efficient.

---

## 3. Summary

- **Threading** outperforms multiprocessing for small-to-medium data chunks, especially with Polars.
- **Multiprocessing** introduces overhead that is only worth it for very large datasets or CPU-bound computations where GIL is limiting.
- Polars demonstrates stronger CPU utilization and faster execution than Pandas for the same tasks.
- Due to Python's Global Interpreter Lock (GIL), multithreading has limited parallel performance for CPU-bound tasks; if the dataset is very large, multiprocessing is preferred for computationally intensive operations.
