
import time
import logging
from contextlib import ContextDecorator
from functools import wraps
from typing import Optional, Dict, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class DebugTimer(ContextDecorator):
    """Context manager and decorator for timing operations"""
    
    def __init__(self, operation_name: str, log_level: str = 'info'):
        self.operation_name = operation_name
        self.log_level = log_level
        self.start_time = None
        self.elapsed = None
        
        # Statistics tracking
        self.stats = defaultdict(list)

    def __enter__(self):
        self.start_time = time.time()
        self._log(f"STARTING: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time
        
        if exc_type:
            self._log(f"FAILED: {self.operation_name} after {self.elapsed:.2f}s - {exc_val}")
        else:
            self._log(f"COMPLETED: {self.operation_name} in {self.elapsed:.2f}s")
            
        # Track statistics
        self.stats[self.operation_name].append(self.elapsed)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper

    def _log(self, message: str):
        """Log message at specified level"""
        log_func = getattr(logger, self.log_level.lower(), logger.info)
        log_func(message)

    def get_stats(self) -> Dict[str, Any]:
        """Get timing statistics"""
        stats = {}
        for op_name, times in self.stats.items():
            if times:
                stats[op_name] = {
                    'count': len(times),
                    'total': sum(times),
                    'average': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times),
                    'last': times[-1]
                }
        return stats

    def reset(self):
        """Reset statistics"""
        self.stats.clear()


class PerformanceMonitor:
    """Monitor performance of multiple operations"""
    
    def __init__(self):
        self.timers: Dict[str, DebugTimer] = {}
        self.results: Dict[str, list] = defaultdict(list)

    def start(self, operation: str) -> DebugTimer:
        """Start timing an operation"""
        timer = DebugTimer(operation)
        timer.__enter__()
        self.timers[operation] = timer
        return timer

    def stop(self, operation: str) -> float:
        """Stop timing an operation"""
        if operation in self.timers:
            timer = self.timers.pop(operation)
            timer.__exit__(None, None, None)
            self.results[operation].append(timer.elapsed)
            return timer.elapsed
        return 0.0

    def get_report(self) -> Dict[str, Any]:
        """Get performance report"""
        report = {}
        for operation, times in self.results.items():
            if times:
                report[operation] = {
                    'count': len(times),
                    'total_time': sum(times),
                    'average_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times)
                }
        return report

    def print_report(self):
        """Print performance report"""
        report = self.get_report()
        
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)
        
        for operation, stats in report.items():
            print(f"\n{operation}:")
            print(f"  Count: {stats['count']}")
            print(f"  Total: {stats['total_time']:.2f}s")
            print(f"  Average: {stats['average_time']:.2f}s")
            print(f"  Min: {stats['min_time']:.2f}s")
            print(f"  Max: {stats['max_time']:.2f}s")
        
        print("\n" + "="*60)


def time_function(func):
    """Decorator to time a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        timer = DebugTimer(func.__name__)
        with timer:
            return func(*args, **kwargs)
    return wrapper


class ProgressTracker:
    """Track progress of long-running operations"""
    
    def __init__(self, total: int, description: str = "Progress"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.last_update = self.start_time

    def update(self, amount: int = 1):
        """Update progress"""
        self.current += amount
        self.last_update = time.time()

    def get_progress(self) -> float:
        """Get progress percentage"""
        return (self.current / self.total) * 100 if self.total > 0 else 0

    def get_eta(self) -> float:
        """Get estimated time remaining in seconds"""
        if self.current == 0:
            return 0
        
        elapsed = time.time() - self.start_time
        rate = self.current / elapsed
        remaining = (self.total - self.current) / rate if rate > 0 else 0
        
        return remaining

    def format_eta(self) -> str:
        """Format ETA as human-readable string"""
        eta = self.get_eta()
        
        if eta < 60:
            return f"{eta:.0f}s"
        elif eta < 3600:
            return f"{eta/60:.1f}m"
        else:
            return f"{eta/3600:.1f}h"

    def get_status(self) -> Dict[str, Any]:
        """Get status dictionary"""
        return {
            'description': self.description,
            'current': self.current,
            'total': self.total,
            'percentage': self.get_progress(),
            'elapsed': time.time() - self.start_time,
            'eta': self.get_eta(),
            'eta_formatted': self.format_eta()
        }

    def print_status(self):
        """Print current status"""
        status = self.get_status()
        print(f"\r{status['description']}: {status['current']}/{status['total']} "
              f"({status['percentage']:.1f}%) - ETA: {status['eta_formatted']}", end='')