"""
Task model for Thread Pool Management System.

Defines TaskStatus enum and Task dataclass with execution support.
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Callable, Any, Optional, Dict
from datetime import datetime
import uuid

class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    TIMEOUT = "Timeout"
    CANCELLED = "Cancelled"

@dataclass
class Task:
    """Represents a single task for the thread pool."""
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    id: str = None
    priority: int = 0  # Lower number = higher priority
    timeout: Optional[int] = None  # Timeout in seconds, None = unlimited
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    created_time: datetime = None
    started_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())[:8]
        if self.kwargs is None:
            self.kwargs = {}
        if self.created_time is None:
            self.created_time = datetime.now()
    
    def set_status(self, status: TaskStatus, result: Any = None, error: str = None):
        """Update task status and timings."""
        self.status = status
        if status == TaskStatus.RUNNING:
            self.started_time = datetime.now()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.TIMEOUT]:
            self.completed_time = datetime.now()
        if result is not None:
            self.result = result
        if error is not None:
            self.error = error
    
    def elapsed_time(self) -> float:
        """Return elapsed time in seconds."""
        if self.completed_time:
            return (self.completed_time - self.created_time).total_seconds()
        elif self.started_time:
            return (datetime.now() - self.created_time).total_seconds()
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dict for UI/logging."""
        data = asdict(self)
        data['status'] = self.status.value
        data['elapsed_time'] = self.elapsed_time()
        data['timeout'] = self.timeout
        data['created_time'] = self.created_time.isoformat()
        if self.started_time:
            data['started_time'] = self.started_time.isoformat()
        if self.completed_time:
            data['completed_time'] = self.completed_time.isoformat()
        return data
    
    def execute(self, timeout: Optional[int] = None) -> tuple[TaskStatus, Any, Optional[str]]:
        """Execute the task function with timeout handling (Windows-compatible)."""
        import concurrent.futures
        from concurrent.futures import TimeoutError as FuturesTimeoutError
        
        effective_timeout = timeout or self.timeout
        self.set_status(TaskStatus.RUNNING)
        
        def target():
            return self.func(*self.args, **self.kwargs)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(target)
            try:
                result = future.result(timeout=effective_timeout)
                self.set_status(TaskStatus.COMPLETED, result=result)
                return TaskStatus.COMPLETED, result, None
            except FuturesTimeoutError:
                self.set_status(TaskStatus.TIMEOUT, error=f"Task {self.id} timed out after {effective_timeout}s")
                future.cancel()
                return TaskStatus.TIMEOUT, None, f"Timeout after {effective_timeout}s"
            except Exception as e:
                self.set_status(TaskStatus.FAILED, error=str(e))
                return TaskStatus.FAILED, None, str(e)

# Example tasks for demo (10 types)
def fibonacci(n: int) -> int:
    """CPU-bound recursive fibonacci."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def sleep_print(seconds: float, message: str = "Hello from worker"):
    """IO-bound sleep with print."""
    import time
    from threading import current_thread
    time.sleep(seconds)
    print(f"[{current_thread().name}] {message}")
    return f"Slept {seconds}s: {message}"

def error_task():
    """Intentional failure."""
    raise ValueError("Intentional error for testing")

def matrix_multiply(size: int) -> str:
    """CPU-bound matrix multiply simulation."""
    import random, time

    a = [[random.random() for _ in range(size)] for _ in range(size)]
    b = [[random.random() for _ in range(size)] for _ in range(size)]
    result = [[0.0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            row_a = a[i]
            total = 0.0
            for k in range(size):
                total += row_a[k] * b[k][j]
            result[i][j] = total

    time.sleep(0.1 * size)
    return f"Matrix {size}x{size} multiplied"

def prime_check(n: int) -> bool:
    """Prime number check (mixed)."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def string_reverse(text: str) -> str:
    """String processing."""
    import time
    time.sleep(0.5)
    return text[::-1]

def json_parse(size: int) -> str:
    """JSON simulation IO."""
    import json, time
    data = {'items': [{'id': i} for i in range(size)]}
    time.sleep(0.2 * size / 1000)
    return json.dumps(data)[:100] + "..."

def file_simulate(filename: str, size: int) -> str:
    """File IO simulation."""
    import time
    time.sleep(size / 1000)
    return f"Simulated write to {filename} ({size}KB)"

def math_sum(n: int) -> int:
    """Math computation."""
    import math
    return sum(math.factorial(i) for i in range(n))

def sort_list(n: int) -> str:
    """Sorting CPU."""
    import random, time
    lst = [random.randint(1, 1000) for _ in range(n)]
    lst.sort()
    time.sleep(0.1 * n / 100)
    return f"Sorted list of {n} elements"

