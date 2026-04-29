"""
Main entry point for Thread Pool Management System.

Launches UI and demonstrates the system.
"""

import sys
from thread_pool import ThreadPool
from ui import ThreadPoolUI
from task import fibonacci, sleep_print, error_task

def main():
    """Main function."""
    print("🧵 Starting Thread Pool Management System...")
    print("Launching GUI... Run 'python main.py' from project root.")
    
    pool = ThreadPool(num_workers=4, default_timeout=60)
    
    ui = ThreadPoolUI(pool)
    
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\\nShutting down gracefully...")
    finally:
        pool.shutdown(wait=True)
        print("✅ Thread Pool Management System stopped.")

if __name__ == "__main__":
    main()

