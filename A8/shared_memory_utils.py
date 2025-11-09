"""
Shared memory footprint monitoring for trading gateway.
Includes CSV logging for performance tracking.
"""

import os
import csv
import time
import psutil
from datetime import datetime
from multiprocessing import shared_memory


# CSV logging
def log_to_csv(filename: str, data: dict):
    """CSV logging function."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    filepath = os.path.join(log_dir, filename)
    file_exists = os.path.exists(filepath)
    
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def get_shared_memory_size(name: str) -> int:
    """Get the size of shared memory region in bytes."""
    try:
        shm = shared_memory.SharedMemory(name=name)
        size = shm.size
        shm.close()
        return size
    except:
        return 0


def get_memory_footprint_mb(name: str) -> float:
    """Get shared memory footprint in MB."""
    size_bytes = get_shared_memory_size(name)
    return size_bytes / (1024 * 1024)


def get_process_memory_mb() -> float:
    """Get current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


def print_memory_usage(shared_memory_name: str, symbols_count: int = 0):
    """Print memory usage report."""
    shared_mb = get_memory_footprint_mb(shared_memory_name)
    process_mb = get_process_memory_mb()
    
    print(f"[MEMORY] Shared memory ({shared_memory_name}): {shared_mb:.6f} MB")
    print(f"[MEMORY] Process memory: {process_mb:.2f} MB")
    
    if symbols_count > 0:
        expected_mb = symbols_count * 8 / (1024 * 1024)  # 8 bytes per symbol
        print(f"[MEMORY] Expected for {symbols_count} symbols: {expected_mb:.6f} MB")


def log_memory_usage(component: str, shared_memory_name: str = ""):
    """Log memory usage to CSV."""
    timestamp = time.time()
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    shared_mb = get_memory_footprint_mb(shared_memory_name) if shared_memory_name else 0
    process_mb = get_process_memory_mb()
    
    data = {
        'timestamp': timestamp,
        'datetime': datetime_str,
        'component': component,
        'shared_memory_mb': shared_mb,
        'process_memory_mb': process_mb,
        'shared_memory_name': shared_memory_name
    }
    
    log_to_csv('memory_usage.csv', data)


def log_latency(component: str, tick_id: int, processing_latency: float, 
                decision_latency: float, symbol: str = ""):
    """Log latency metrics to CSV."""
    timestamp = time.time()
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    data = {
        'timestamp': timestamp,
        'datetime': datetime_str,
        'component': component,
        'tick_id': tick_id,
        'processing_latency_ms': processing_latency * 1000,
        'decision_latency_ms': decision_latency * 1000,
        'symbol': symbol
    }
    
    log_to_csv('latency_metrics.csv', data)


def log_throughput(component: str, price_tps: float, news_tps: float, total_ticks: int):
    """Log throughput metrics to CSV."""
    timestamp = time.time()
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    data = {
        'timestamp': timestamp,
        'datetime': datetime_str,
        'component': component,
        'price_ticks_per_sec': price_tps,
        'news_ticks_per_sec': news_tps,
        'total_ticks': total_ticks
    }
    
    log_to_csv('throughput_metrics.csv', data)
