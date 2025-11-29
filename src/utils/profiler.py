"""
Performance profiling utilities for Backtest Agent.

Provides tools to profile and analyze performance bottlenecks in
agent execution, backtesting, and data operations.
"""

import time
import functools
from typing import Dict, Any, Optional, Callable
from contextlib import contextmanager
import structlog

logger = structlog.get_logger(__name__)


class PerformanceProfiler:
    """
    Performance profiler for tracking execution times and bottlenecks.

    Usage:
        profiler = PerformanceProfiler()

        with profiler.profile("operation_name"):
            # code to profile
            pass

        stats = profiler.get_stats()
    """

    def __init__(self):
        """Initialize the profiler."""
        self.timings: Dict[str, list] = {}
        self.call_counts: Dict[str, int] = {}
        self.enabled = True

    def enable(self):
        """Enable profiling."""
        self.enabled = True

    def disable(self):
        """Disable profiling."""
        self.enabled = False

    def reset(self):
        """Reset all profiling data."""
        self.timings = {}
        self.call_counts = {}

    @contextmanager
    def profile(self, operation_name: str, **metadata):
        """
        Context manager for profiling an operation.

        Args:
            operation_name: Name of the operation
            **metadata: Additional metadata to log

        Yields:
            None
        """
        if not self.enabled:
            yield
            return

        start_time = time.time()

        try:
            yield

        finally:
            duration = time.time() - start_time

            # Record timing
            if operation_name not in self.timings:
                self.timings[operation_name] = []
                self.call_counts[operation_name] = 0

            self.timings[operation_name].append(duration)
            self.call_counts[operation_name] += 1

            # Log
            logger.debug(
                "profiler.operation",
                operation=operation_name,
                duration=duration,
                **metadata
            )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get profiling statistics.

        Returns:
            Dictionary with statistics for each profiled operation
        """
        stats = {}

        for operation, times in self.timings.items():
            if not times:
                continue

            total_time = sum(times)
            count = self.call_counts[operation]
            avg_time = total_time / count if count > 0 else 0
            min_time = min(times)
            max_time = max(times)

            stats[operation] = {
                'total_time': total_time,
                'count': count,
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'total_percent': 0  # Will be calculated after
            }

        # Calculate percentages
        total_all = sum(s['total_time'] for s in stats.values())

        if total_all > 0:
            for operation in stats:
                stats[operation]['total_percent'] = (
                    stats[operation]['total_time'] / total_all * 100
                )

        return stats

    def print_stats(self, top_n: int = 10):
        """
        Print profiling statistics.

        Args:
            top_n: Number of top operations to show
        """
        stats = self.get_stats()

        if not stats:
            print("No profiling data available")
            return

        # Sort by total time
        sorted_stats = sorted(
            stats.items(),
            key=lambda x: x[1]['total_time'],
            reverse=True
        )

        print("\n" + "=" * 80)
        print("Performance Profile")
        print("=" * 80)
        print(
            f"{'Operation':<40} {'Count':>8} {'Total (s)':>12} "
            f"{'Avg (s)':>12} {'%':>6}"
        )
        print("-" * 80)

        for operation, data in sorted_stats[:top_n]:
            print(
                f"{operation:<40} {data['count']:>8} "
                f"{data['total_time']:>12.4f} "
                f"{data['avg_time']:>12.4f} "
                f"{data['total_percent']:>6.1f}"
            )

        print("=" * 80 + "\n")

    def get_bottlenecks(self, threshold_percent: float = 5.0) -> list:
        """
        Identify performance bottlenecks.

        Args:
            threshold_percent: Operations taking more than this % of total time

        Returns:
            List of bottleneck operations
        """
        stats = self.get_stats()
        bottlenecks = []

        for operation, data in stats.items():
            if data['total_percent'] >= threshold_percent:
                bottlenecks.append({
                    'operation': operation,
                    'total_time': data['total_time'],
                    'percent': data['total_percent'],
                    'avg_time': data['avg_time'],
                    'count': data['count']
                })

        # Sort by percent
        bottlenecks.sort(key=lambda x: x['percent'], reverse=True)

        return bottlenecks


# Global profiler instance
_global_profiler = None


def get_profiler() -> PerformanceProfiler:
    """
    Get the global profiler instance.

    Returns:
        PerformanceProfiler instance
    """
    global _global_profiler

    if _global_profiler is None:
        _global_profiler = PerformanceProfiler()

    return _global_profiler


@contextmanager
def profile(operation_name: str, **metadata):
    """
    Profile an operation using the global profiler.

    Args:
        operation_name: Name of the operation
        **metadata: Additional metadata

    Yields:
        None
    """
    with get_profiler().profile(operation_name, **metadata):
        yield


def profile_function(operation_name: Optional[str] = None):
    """
    Decorator to profile a function.

    Args:
        operation_name: Optional operation name (defaults to function name)

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = operation_name or f"{func.__module__}.{func.__name__}"

            with profile(name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


class Timer:
    """
    Simple timer for measuring execution time.

    Usage:
        timer = Timer()
        timer.start()
        # ... code ...
        elapsed = timer.stop()
    """

    def __init__(self):
        """Initialize the timer."""
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start the timer."""
        self.start_time = time.time()
        self.end_time = None

    def stop(self) -> float:
        """
        Stop the timer and return elapsed time.

        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            raise RuntimeError("Timer not started")

        self.end_time = time.time()
        return self.elapsed()

    def elapsed(self) -> float:
        """
        Get elapsed time.

        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            return 0.0

        end = self.end_time if self.end_time is not None else time.time()
        return end - self.start_time

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def time_function(func: Callable) -> Callable:
    """
    Decorator to time a function and log the result.

    Args:
        func: Function to time

    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timer = Timer()
        timer.start()

        try:
            result = func(*args, **kwargs)
            duration = timer.stop()

            logger.info(
                "function.timed",
                function=func.__name__,
                duration=duration
            )

            return result

        except Exception as e:
            duration = timer.stop()

            logger.error(
                "function.timed.error",
                function=func.__name__,
                duration=duration,
                error=str(e)
            )

            raise

    return wrapper


def benchmark(
    func: Callable,
    iterations: int = 100,
    warmup: int = 10
) -> Dict[str, float]:
    """
    Benchmark a function by running it multiple times.

    Args:
        func: Function to benchmark (should take no arguments)
        iterations: Number of iterations
        warmup: Number of warmup iterations

    Returns:
        Dictionary with benchmark statistics
    """
    # Warmup
    for _ in range(warmup):
        func()

    # Benchmark
    times = []

    for _ in range(iterations):
        timer = Timer()
        timer.start()
        func()
        times.append(timer.stop())

    import numpy as np

    return {
        'iterations': iterations,
        'total_time': sum(times),
        'mean_time': np.mean(times),
        'median_time': np.median(times),
        'std_time': np.std(times),
        'min_time': min(times),
        'max_time': max(times),
        'throughput': iterations / sum(times)  # ops per second
    }
