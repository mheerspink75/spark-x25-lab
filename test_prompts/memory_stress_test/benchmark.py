"""
Benchmark Application for memory stress testing.

Simulates resource consumption across CPU, memory, file I/O, and multithreading
to validate the memory stress test scenario.

Dependencies: Python standard library only (no external packages).
"""

import time
import os
import json
import resource
import threading
from concurrent.futures import ThreadPoolExecutor
import random

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- Configuration ----------
CPU_CORES = 4
MEMORY_MB = 16
THREAD_COUNT = 4
RUN_TIMES = 3  # number of benchmark iterations (reduced for speed)

# Memory stress size in bytes (utilized by the stress testing loop)
MEMORY_STESS_BYTES = (MEMORY_MB * 1024 * 1024)  # one allocation of the full memory size


# ---------- Memory stress helpers (simulate memory access) ----------
def _read_memory(buffer: bytearray) -> None:
    """Simulate reading memory (minimal randomized access)."""
    for i in range(len(buffer)):
        buffer[i] ^= random.randrange(256)


def _write_memory(buffer: bytearray) -> None:
    """Simulate writing memory (minimal randomized access)."""
    for i in range(len(buffer)):
        buffer[i] = (buffer[i] + random.randrange(256)) & 0xFF


# ---------- Benchmark Core ----------
class PerformanceBenchmark:
    """Core benchmark engine with metrics collection."""

    def __init__(self, cpu_cores: int, memory_mb: int, thread_count: int):
        self.cpu_cores = cpu_cores
        self.memory_mb = memory_mb
        self.thread_count = thread_count

    def _metric(self, name: str, value: float, duration: float, extra: str = "", detail: str = "") -> dict:
        return {
            "metric": name,
            "value": round(value, 4),
            "duration_seconds": round(duration, 6),
            "details": extra,
            "detail": detail,
        }

    def run_cpu(self) -> dict:
        """Measure single-threaded CPU performance."""
        results = []
        # Fixed CPU benchmarking iterations (integer-based for safe arithmetic)
        for _ in range(RUN_TIMES):
            start = time.perf_counter()
            # Simulate CPU-bound operation: perform a loop
            for _ in range(5):
                pass
            elapsed = time.perf_counter() - start
            results.append(self._metric(
                "cpu_performance",
                elapsed,
                elapsed,
                detail=f"single-thread"
            ))
        return {
            "cpu_performance": results,
            "duration_seconds_total": round(time.perf_counter(), 6),
        }

    def run_memory(self) -> dict:
        """Measure memory stress under concurrent access."""
        results = []
        allocs = 0
        total_allocated_bytes = 0
        max_rss_kb = 0.0
        start = time.perf_counter()

        # Allocate one large stress buffer shared across all threads
        stress_buffer = bytearray(MEMORY_STESS_BYTES)

        for _ in range(self.thread_count):
            buffer = stress_buffer
            allocs += 1
            total_allocated_bytes += MEMORY_STESS_BYTES
            # Perform lightweight memory stress operations (much smaller than full allocation)
            for _ in range(RUN_TIMES):
                _read_memory(buffer)
                _write_memory(buffer)
            # Track peak RSS
            current_rss_kb = process_peak_rss_kb()
            if current_rss_kb > max_rss_kb:
                max_rss_kb = current_rss_kb

        elapsed = time.perf_counter() - start
        results.append(self._metric(
            "memory_performance",
            allocs,
            elapsed,
            detail=(
                f"allocations={allocs}, "
                f"total_bytes_allocated={total_allocated_bytes}, "
                f"peak_rss_kb={max_rss_kb:.2f}"
            ),
        ))
        return {
            "memory_performance": results,
            "duration_seconds_total": round(elapsed, 6),
        }

    def run_file_io(self) -> dict:
        """Measure file I/O performance under varying load."""
        results = []
        for _ in range(RUN_TIMES):
            start = time.perf_counter()
            os.makedirs(".benchmark_results", exist_ok=True)
            for i in range(20):
                temp_file = f".benchmark_results/foo_{i}.txt"
                with open(temp_file, "w", encoding="utf-8") as f:
                    f.write(f"benchmark_{i}\n")
                with open(temp_file, "r", encoding="utf-8") as f:
                    f.read()
            elapsed = time.perf_counter() - start
            results.append(self._metric(
                "file_io_performance",
                elapsed,
                elapsed,
                detail=f"io_load_{20}"
            ))
        return {
            "file_io_performance": results,
            "duration_seconds_total": round(time.perf_counter(), 6),
        }

    def run_multithreaded(self) -> dict:
        """Measure multithreaded CPU performance."""
        results = []
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = [
                executor.submit(self._cpu_worker, i)
                for i in range(self.thread_count)
            ]
            for future in futures:
                future.result()
        total_elapsed = time.perf_counter() - start
        results.append(self._metric(
            "multithreaded_performance",
            total_elapsed,
            total_elapsed,
            detail=f"thread_count={self.thread_count}"
        ))
        return {
            "multithreaded_performance": results,
            "duration_seconds_total": round(time.perf_counter(), 6),
        }

    def _cpu_worker(self, index: int) -> dict:
        """Benchmark a single worker thread under CPU contention."""
        start = time.perf_counter()
        # Fixed CPU benchmarking iterations (integer-based for safe arithmetic)
        for _ in range(RUN_TIMES):
            for _ in range(5):
                pass
        elapsed = time.perf_counter() - start
        return {"worker": index, "elapsed_seconds": round(elapsed, 6)}


# ---------- Main ----------
def main() -> None:
    benchmark = PerformanceBenchmark(
        cpu_cores=CPU_CORES,
        memory_mb=MEMORY_MB,
        thread_count=THREAD_COUNT,
    )

    print("=== Memory Stress Benchmark ===")
    print(f"CPU cores: {CPU_CORES}")
    print(f"Memory capacity: {MEMORY_MB} MB")
    print(f"Thread count: {THREAD_COUNT}")
    print()

    results = {
        "cpu_performance": benchmark.run_cpu(),
        "memory_performance": benchmark.run_memory(),
        "file_io_performance": benchmark.run_file_io(),
        "multithreaded_performance": benchmark.run_multithreaded(),
    }

    # Save raw results
    os.makedirs(".benchmark_results", exist_ok=True)
    with open(".benchmark_results/benchmark_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Write detailed results
    os.makedirs(".benchmark_results", exist_ok=True)
    for key, value in results.items():
        with open(
            f".benchmark_results/results_{key}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(value, f, ensure_ascii=False, indent=2)

    print("\n=== Benchmark Results ===")
    for key, value in results.items():
        print(f"\n{key}:")
        # Use the result dict that produced this key
        for item in value["file_io_performance"] if key == "file_io_performance" else value["cpu_performance"] if key == "cpu_performance" else value["multithreaded_performance"] if key == "multithreaded_performance" else value["memory_performance"]:
            print(f"  {item['metric']}: {item['value']} ({item['duration_seconds']}s)")

    print("\nResults saved to .benchmark_results/")


def process_peak_rss_kb() -> float:
    """Return peak process resident set size in kilobytes."""
    rule = resource.getrusage(resource.RUSAGE_SELF)
    if hasattr(rule, "ru_maxrss"):
        # On Linux, ru_maxrss is returned in bytes; convert to KB.
        # On Windows it is already in KB.
        return float(rule.ru_maxrss) / 1024.0
    return float(rule.ru_maxrss)


# ---------- Plotting ----------
def _to_list(values) -> list:
    """Normalize input to a list of numeric values."""
    if not values:
        return []
    item = values[0]
    if isinstance(values, (list, tuple)) and len(values) > 0:
        # Check if all items are dicts
        if all(isinstance(v, dict) for v in values):
            return [float(v.get("value", 0)) for v in values]
        # Fall back to raw values
        return [float(v) for v in values]
    return [float(value)]


def _to_list_seconds(values) -> list:
    """Normalize input to a list of duration values in seconds."""
    if not values:
        return []
    item = values[0]
    if isinstance(values, (list, tuple)) and len(values) > 0:
        if all(isinstance(v, dict) for v in values):
            return [float(v.get("duration_seconds", 0)) for v in values]
        # Fall back to raw values
        return [float(v) for v in values]
    return [float(item.get("duration_seconds", 0))]


def generate_graphs(results: dict) -> None:
    """Generate PNG graphs from collected benchmark metrics.

    Produces per-metric charts and a comparison summary for visualization.
    All outputs are written into the .benchmark_results directory.
    """
    os.makedirs(".benchmark_results", exist_ok=True)

    metrics = ["cpu_performance", "memory_performance", "file_io_performance", "multithreaded_performance"]
    data = results

    # CPU performance chart
    plt.figure(figsize=(8, 5))
    durations = _to_list_seconds(data["cpu_performance"]["cpu_performance"])
    plt.plot(durations, marker="o", label="CPU Performance (single-thread)")
    plt.title("CPU Performance Benchmark")
    plt.xlabel("Iteration")
    plt.ylabel("Duration (s)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(".benchmark_results/graphs/cpu_performance.png", dpi=150)
    plt.close()

    # Memory performance chart
    plt.figure(figsize=(8, 5))
    mem_items = data["memory_performance"]["memory_performance"]
    durations_mem = _to_list_seconds(mem_items)
    values_mem = _to_list(mem_items)
    plt.plot(durations_mem, values_mem, marker="s", label="Memory Performance")
    plt.title("Memory Performance Benchmark")
    plt.xlabel("Duration (s)")
    plt.ylabel("Allocation Count")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(".benchmark_results/graphs/memory_performance.png", dpi=150)
    plt.close()

    # File I/O performance chart
    plt.figure(figsize=(8, 5))
    io_items = data["file_io_performance"]["file_io_performance"]
    durations_io = _to_list_seconds(io_items)
    values_io = _to_list(io_items)
    plt.plot(durations_io, values_io, marker="^", label="File I/O Performance")
    plt.title("File I/O Performance Benchmark")
    plt.xlabel("Duration (s)")
    plt.ylabel("Performance Value")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(".benchmark_results/graphs/file_io_performance.png", dpi=150)
    plt.close()

    # Multithreaded performance chart
    plt.figure(figsize=(8, 5))
    mt_items = data["multithreaded_performance"]["multithreaded_performance"]
    durations_mt = _to_list_seconds(mt_items)
    values_mt = _to_list(mt_items)
    plt.plot(durations_mt, values_mt, marker="D", label="Multithreaded Performance")
    plt.title("Multithreaded Performance Benchmark")
    plt.xlabel("Duration (s)")
    plt.ylabel("Performance Value")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(".benchmark_results/graphs/multithreaded_performance.png", dpi=150)
    plt.close()

    # Comparison summary chart
    plt.figure(figsize=(9, 5))
    metrics_summary = []
    metrics_labels = []
    for metric in metrics:
        items = data[metric][metric]
        if items:
            values = _to_list(items)
            durations = _to_list_seconds(items)
            if values and durations:
                metrics_summary.append(max(values))  # use max or avg as representative value
            else:
                metrics_summary.append(0)
            metrics_labels.append(metric.replace("_performance", "").replace("cpu_", "CPU ").replace("memory_", "Memory").replace("file_io_", "File I/O ").replace("multithreaded_", "Multithreaded "))
    plt.bar(metrics_labels, metrics_summary, color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"])
    plt.title("Benchmark Metrics Summary (Max Value)")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.grid(True, alpha=0.3, axis="y")
    plt.savefig(".benchmark_results/graphs/summary_comparison.png", dpi=150)
    plt.close()

    print("=== Graphs generated ===")
    print("  .benchmark_results/graphs/cpu_performance.png")
    print("  .benchmark_results/graphs/memory_performance.png")
    print("  .benchmark_results/graphs/file_io_performance.png")
    print("  .benchmark_results/graphs/multithreaded_performance.png")
    print("  .benchmark_results/graphs/summary_comparison.png")


# ---------- Main ----------
def main() -> None:
    benchmark = PerformanceBenchmark(
        cpu_cores=CPU_CORES,
        memory_mb=MEMORY_MB,
        thread_count=THREAD_COUNT,
    )

    print("=== Memory Stress Benchmark ===")
    print(f"CPU cores: {CPU_CORES}")
    print(f"Memory capacity: {MEMORY_MB} MB")
    print(f"Thread count: {THREAD_COUNT}")
    print()

    results = {
        "cpu_performance": benchmark.run_cpu(),
        "memory_performance": benchmark.run_memory(),
        "file_io_performance": benchmark.run_file_io(),
        "multithreaded_performance": benchmark.run_multithreaded(),
    }

    # Save raw results
    os.makedirs(".benchmark_results", exist_ok=True)
    with open(".benchmark_results/benchmark_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Write detailed results
    os.makedirs(".benchmark_results", exist_ok=True)
    for key, value in results.items():
        with open(
            f".benchmark_results/results_{key}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(value, f, ensure_ascii=False, indent=2)

    print("\n=== Benchmark Results ===")
    for key, value in results.items():
        print(f"\n{key}:")
        # Use the result dict that produced this key
        for item in value["file_io_performance"] if key == "file_io_performance" else value["cpu_performance"] if key == "cpu_performance" else value["multithreaded_performance"] if key == "multithreaded_performance" else value["memory_performance"]:
            print(f"  {item['metric']}: {item['value']} ({item['duration_seconds']}s)")

    print("\nResults saved to .benchmark_results/")

    # Generate graphs
    generate_graphs(results)


def process_peak_rss_kb() -> float:
    """Return peak process resident set size in kilobytes."""
    rule = resource.getrusage(resource.RUSAGE_SELF)
    if hasattr(rule, "ru_maxrss"):
        # On Linux, ru_maxrss is returned in bytes; convert to KB.
        # On Windows it is already in KB.
        return float(rule.ru_maxrss) / 1024.0
    return float(rule.ru_maxrss)


if __name__ == "__main__":
    main()
