"""
Worker thread implementation for the thread pool.

Workers continuously poll the queue and execute tasks.
"""

import logging
import threading
from typing import Optional
from task import Task, TaskStatus
from queue_manager import TaskQueue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('threadpool.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Worker(threading.Thread):
    """Worker thread that executes tasks from the queue."""
    
    def __init__(self, queue: TaskQueue, name: str):
        super().__init__(name=name, daemon=True)
        self.queue = queue
        self.active = True
    
    def run(self):
        """Main worker loop."""
        logger.info(f"Worker {self.name} started")
        while self.active:
            task = self.queue.get_task(timeout=1.0)
            if task is None:  # Timeout or sentinel
                continue
            
            logger.info(f"Worker {self.name} picked task {task.id}")
            
            if task.status == TaskStatus.CANCELLED:
                logger.info(f"Skipping cancelled task {task.id}")
                continue
            
            # Execute task using task's timeout
            status, result, error = task.execute(timeout=task.timeout)
            
            if status == TaskStatus.COMPLETED:
                logger.info(f"Task {task.id} completed: {result}")
            elif status == TaskStatus.FAILED:
                logger.error(f"Task {task.id} failed: {error}")
            elif status == TaskStatus.TIMEOUT:
                logger.warning(f"Task {task.id} timeout: {error}")
        
        logger.info(f"Worker {self.name} stopped")
    
    def stop(self):
        """Signal worker to stop."""
        self.active = False

