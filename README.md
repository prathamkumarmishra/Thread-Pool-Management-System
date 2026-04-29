# 🧵 Thread Pool Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

A complete, production-ready **Thread Pool Management System** implemented in Python for Operating Systems academic projects. Features multithreading, priority queue, real-time Tkinter GUI, comprehensive logging, error handling, and timeout support.

## 🎯 Features

- ✅ **Fixed Thread Pool** (configurable workers)
- ✅ **Priority Task Queue** (PriorityQueue)
- ✅ **Task Status Tracking** (Pending/Running/Completed/Failed/Timeout)
- ✅ **Real-time Tkinter GUI** dashboard
- ✅ **Example Tasks**: CPU-bound (Fibonacci), IO-bound (Sleep), Error cases
- ✅ **Timeout Handling** (30s per task)
- ✅ **Comprehensive Logging** (file + console)
- ✅ **Thread-safe Stats** & Monitoring
- ✅ **Graceful Shutdown**
- ✅ **OOP Design** with dataclasses/enums/typing

## 📁 Project Structure

```
OSProject/
├── task.py          # Task model + status enum + examples
├── queue_manager.py # PriorityQueue wrapper
├── worker.py        # Worker thread implementation
├── thread_pool.py   # Main ThreadPool manager
├── ui.py            # Tkinter GUI dashboard
├── main.py          # Entry point
├── TODO.md          # Implementation tracker
├── README.md        # 📄 You are here
└── threadpool.log   # Generated log file
```

## 🚀 Quick Start

1. **No dependencies needed** (pure stdlib Python 3.8+)
2. **Run the demo**:
   ```bash
   cd "c:/Users/Dev Mishra/OneDrive/Desktop/OSProject"
   python main.py
   ```

3. **GUI Features**:
   - Real-time task list with status/priority/elapsed time
   - Live pool stats (active threads, queue size, etc.)
   - Add custom tasks (fibonacci, sleep, error)
   - Auto-adds sample tasks on startup

## 🖥️ Sample Output

```
🧵 Starting Thread Pool Management System...
2024-XX-XX [Worker-1] INFO: Worker Worker-1 started
Added task abc123 (priority 5)
Added task def456 (priority 1)
[Worker-2] Task abc123 picked...
[main] Launching GUI...
```

**GUI Screenshot** (modern dark theme):
- Stats bar: Active Threads: 4 | Queue: 0 | Total Tasks: 3
- Tasks table updates live as fib(28) computes, sleep tasks finish
- Add more via dropdown + priority spinner

## 🏗️ Architecture Overview

```
Main.py → ThreadPool(4) → 4x Worker Threads
                ↓
           TaskQueue (PriorityQueue)
                ↓
           Tasks: func(args) + status tracking
                ↓
            ui.py (Tkinter polling @1s)
```

```
Task Flow:
1. add_task(func, args, priority) → Task() → queue.put((-priority, id, task))
2. Worker: queue.get() → task.execute(30s timeout)
3. Status update → stats refresh → GUI poll → display
```

## 🔧 Customization

- **Worker Count**: `ThreadPool(num_workers=8)`
- **Task Timeout**: Modify `task.py::execute(timeout=60)`
- **New Tasks**: Add to `task.py`, update ui.py combobox
- **Priority**: Negative = higher priority (-10 max, 10 min)

## 📊 Performance Notes (OS Project Viva)

- **Avoids Thread Creation Overhead**: Fixed workers poll queue
- **PriorityQueue**: O(log n) insert/pop, heap-based
- **Thread-Safety**: Locks for stats/tasks dict
- **GIL Impact**: Good for IO-bound; CPU via multiprocessing bonus
- **Demo Comparison**: Sequential vs Pool (add to main.py)

## 🧪 Testing

1. **CPU Test**: Fibonacci(30) - watches RUNNING → COMPLETED
2. **IO Test**: sleep_print(5.0) - low priority
3. **Error Test**: error_task() → FAILED
4. **Timeout**: Modify fib(40) >30s → TIMEOUT
5. **Shutdown**: Ctrl+C → graceful worker joins

## 📝 Academic Evaluation Points

1. **Multithreading Concepts**: Thread pools, race conditions (mitigated by locks), daemon threads
2. **Synchronization**: Queue, Lock primitives
3. **Priority Scheduling**: Heap queue simulation
4. **Process vs Thread**: GUI main thread + workers
5. **Error/Timeout Handling**: Signals for alarm
6. **Real-time Systems**: Polling GUI updates

## 🔮 Bonus Implemented

- Performance-ready logging
- Dark-themed attractive UI
- Complete OOP with typing
- Context manager support (`with ThreadPool(): ...`)

## 🤔 Troubleshooting

- **Tkinter not found**: `pip install tk` (rare, stdlib)
- **PermissionError**: Run VSCode as admin
- **No GUI**: Ensure X11/Wayland (Linux) or Windows display
- **Logs**: Check `threadpool.log`

---

**Built for OS Academic Excellence** 🎓 | **Zero Dependencies** | **Production Patterns**

**Run `python main.py` now!**

