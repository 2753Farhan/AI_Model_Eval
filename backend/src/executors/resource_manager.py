
from typing import Dict, Any, Optional
import psutil
import os
import threading
import time
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ResourceLimits:
    """Resource limits for execution"""
    max_cpu_percent: float = 80.0
    max_memory_mb: float = 1024.0
    max_disk_mb: float = 1024.0
    max_processes: int = 10
    max_execution_time: int = 60


@dataclass
class ResourceUsage:
    """Resource usage statistics"""
    cpu_percent: float
    memory_mb: float
    disk_mb: float
    process_count: int
    execution_time: float


class ResourceManager:
    """Manages system resources"""
    
    def __init__(self, limits: Optional[ResourceLimits] = None):
        self.limits = limits or ResourceLimits()
        self.processes: Dict[int, Dict[str, Any]] = {}
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

    def check_resources(self) -> Dict[str, Any]:
        """Check current resource usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_mb = memory.used / (1024 * 1024)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_mb = disk.used / (1024 * 1024)
            
            # Process count
            process_count = len(psutil.pids())
            
            return {
                'cpu_percent': cpu_percent,
                'memory_mb': memory_mb,
                'memory_percent': memory.percent,
                'disk_mb': disk_mb,
                'disk_percent': disk.percent,
                'process_count': process_count,
                'available_memory_mb': memory.available / (1024 * 1024)
            }
            
        except Exception as e:
            logger.error(f"Failed to check resources: {e}")
            return {
                'cpu_percent': 0,
                'memory_mb': 0,
                'process_count': 0,
                'error': str(e)
            }

    def can_execute(self, estimated_memory_mb: float = 100) -> bool:
        """Check if we can execute a new process"""
        resources = self.check_resources()
        
        with self.lock:
            # Check CPU
            if resources.get('cpu_percent', 0) > self.limits.max_cpu_percent:
                logger.warning(f"CPU usage too high: {resources['cpu_percent']}%")
                return False
            
            # Check memory
            if resources.get('memory_mb', 0) + estimated_memory_mb > self.limits.max_memory_mb:
                logger.warning(f"Memory usage would exceed limit")
                return False
            
            # Check process count
            if resources.get('process_count', 0) > self.limits.max_processes:
                logger.warning(f"Too many processes: {resources['process_count']}")
                return False
            
            return True

    def register_process(self, pid: int, metadata: Dict[str, Any]) -> None:
        """Register a process for monitoring"""
        with self.lock:
            self.processes[pid] = {
                'pid': pid,
                'start_time': time.time(),
                'metadata': metadata,
                'status': 'running'
            }
        logger.info(f"Registered process {pid}")

    def unregister_process(self, pid: int) -> None:
        """Unregister a process"""
        with self.lock:
            if pid in self.processes:
                self.processes[pid]['status'] = 'completed'
                self.processes[pid]['end_time'] = time.time()
                logger.info(f"Unregistered process {pid}")

    def get_process_stats(self, pid: int) -> Optional[Dict[str, Any]]:
        """Get statistics for a process"""
        try:
            process = psutil.Process(pid)
            
            with process.oneshot():
                cpu_percent = process.cpu_percent(interval=0.1)
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)
                
                stats = {
                    'pid': pid,
                    'cpu_percent': cpu_percent,
                    'memory_mb': memory_mb,
                    'status': process.status(),
                    'create_time': process.create_time(),
                    'num_threads': process.num_threads()
                }
                
                # Add registered metadata if available
                with self.lock:
                    if pid in self.processes:
                        stats.update(self.processes[pid].get('metadata', {}))
                
                return stats
                
        except psutil.NoSuchProcess:
            return None
        except Exception as e:
            logger.error(f"Failed to get process stats for {pid}: {e}")
            return None

    def kill_process(self, pid: int) -> bool:
        """Kill a process"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            
            # Wait for termination
            gone, alive = psutil.wait_procs([process], timeout=3)
            if alive:
                process.kill()
            
            self.unregister_process(pid)
            logger.info(f"Killed process {pid}")
            return True
            
        except psutil.NoSuchProcess:
            self.unregister_process(pid)
            return True
        except Exception as e:
            logger.error(f"Failed to kill process {pid}: {e}")
            return False

    def kill_all_processes(self) -> None:
        """Kill all registered processes"""
        with self.lock:
            pids = list(self.processes.keys())
        
        for pid in pids:
            self.kill_process(pid)

    def start_monitoring(self, interval: float = 5.0) -> None:
        """Start resource monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        logger.info("Resource monitoring started")

    def stop_monitoring(self) -> None:
        """Stop resource monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        logger.info("Resource monitoring stopped")

    def _monitor_loop(self, interval: float) -> None:
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Check system resources
                resources = self.check_resources()
                
                # Check registered processes
                with self.lock:
                    for pid in list(self.processes.keys()):
                        stats = self.get_process_stats(pid)
                        if stats:
                            self.processes[pid]['last_stats'] = stats
                        else:
                            # Process died unexpectedly
                            self.processes[pid]['status'] = 'terminated'
                            self.processes[pid]['end_time'] = time.time()
                
                # Check if we need to kill any processes
                if resources.get('cpu_percent', 0) > self.limits.max_cpu_percent * 1.5:
                    logger.warning("CPU usage critical, killing oldest process")
                    self._kill_oldest_process()
                
                if resources.get('memory_mb', 0) > self.limits.max_memory_mb * 1.5:
                    logger.warning("Memory usage critical, killing largest process")
                    self._kill_largest_process()
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
            
            time.sleep(interval)

    def _kill_oldest_process(self) -> None:
        """Kill the oldest running process"""
        with self.lock:
            if not self.processes:
                return
            
            oldest_pid = min(
                self.processes.items(),
                key=lambda x: x[1].get('start_time', float('inf'))
            )[0]
        
        self.kill_process(oldest_pid)

    def _kill_largest_process(self) -> None:
        """Kill the process using most memory"""
        with self.lock:
            if not self.processes:
                return
            
            largest_pid = None
            largest_memory = 0
            
            for pid in self.processes:
                stats = self.get_process_stats(pid)
                if stats and stats.get('memory_mb', 0) > largest_memory:
                    largest_memory = stats['memory_mb']
                    largest_pid = pid
            
            if largest_pid:
                self.kill_process(largest_pid)

    def get_summary(self) -> Dict[str, Any]:
        """Get resource management summary"""
        resources = self.check_resources()
        
        with self.lock:
            running_processes = [
                p for p in self.processes.values()
                if p.get('status') == 'running'
            ]
            
            return {
                'system': resources,
                'limits': {
                    'max_cpu_percent': self.limits.max_cpu_percent,
                    'max_memory_mb': self.limits.max_memory_mb,
                    'max_disk_mb': self.limits.max_disk_mb,
                    'max_processes': self.limits.max_processes,
                    'max_execution_time': self.limits.max_execution_time
                },
                'processes': {
                    'total': len(self.processes),
                    'running': len(running_processes),
                    'completed': len(self.processes) - len(running_processes)
                },
                'can_execute': self.can_execute()
            }