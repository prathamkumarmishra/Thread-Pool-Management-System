"""
Tkinter GUI for Thread Pool Management System.

Real-time dashboard for tasks and pool stats.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from typing import Dict, Any
from thread_pool import ThreadPool
from task import fibonacci, sleep_print, error_task

class ThreadPoolUI:
    """Main UI class."""
    
    def __init__(self, pool: ThreadPool):
        self.pool = pool
        self.root = tk.Tk()
        self.root.title("Thread Pool Management System")
        self.root.geometry("1200x750")
        self.root.configure(bg="#2b2b2b")
        
        self.setup_ui()
        self.update_loop()
    
    def setup_ui(self):
        """Setup all UI components."""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', background='#2b2b2b', foreground='#ffffff', font=('Arial', 16, 'bold'))
        style.configure('Stats.TLabel', background='#2b2b2b', foreground='#4CAF50', font=('Arial', 12))
        # Treeview selection highlight for dark theme
        style.configure("Treeview", background="#404040", foreground="white", fieldbackground="#404040")
        style.map("Treeview", background=[('selected', '#0078d4')], foreground=[('selected', 'white')])
        
        # Title
        title = ttk.Label(self.root, text="🧵 Thread Pool Management System", style='Title.TLabel')
        title.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg='#2b2b2b')
        stats_frame.pack(pady=5, fill='x', padx=20)
        
        self.stats_labels = {}
        stats = ['active_threads', 'queue_size', 'tasks_total', 'tasks_running', 'tasks_completed', 'tasks_failed', 'tasks_pending']
        for i, stat in enumerate(stats):
            label = ttk.Label(stats_frame, text=f"{stat.replace('_', ' ').title()}: 0", style='Stats.TLabel')
            label.grid(row=i//3, column=(i%3), padx=10, pady=5, sticky='w')
            self.stats_labels[stat] = label
        
        # Tasks frame
        tasks_frame = tk.LabelFrame(self.root, text="📋 Tasks", font=('Arial', 12, 'bold'))
        tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tasks treeview - added Timeout column
        columns = ('ID', 'Status', 'Priority', 'Timeout', 'Function', 'Elapsed', 'Result')
        self.tree = ttk.Treeview(tasks_frame, columns=columns, show='headings', height=15, selectmode='browse')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col == 'ID' else 110)
        
        scrollbar = ttk.Scrollbar(tasks_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Add task frame - added Timeout input
        add_frame = tk.Frame(self.root, bg='#2b2b2b')
        add_frame.pack(fill='x', padx=20, pady=10)
        
        label_add = tk.Label(add_frame, text="Add Task:", bg='#2b2b2b', fg='white', font=('Arial', 10, 'bold'))
        label_add.pack(side='left')
        
        # Task type
        label_type = tk.Label(add_frame, text="Type:", bg='#2b2b2b', fg='white')
        label_type.pack(side='left', padx=5)
        self.task_var = tk.StringVar(value="fibonacci")
        task_combo = ttk.Combobox(add_frame, textvariable=self.task_var, values=[
            "fibonacci", "sleep_print", "error_task", 
            "matrix_multiply", "prime_check", "string_reverse", 
            "json_parse", "file_simulate", "math_sum", "sort_list"
        ], state="readonly", width=12)
        task_combo.pack(side='left', padx=5)
        
        # Args
        label_arg = tk.Label(add_frame, text="Arg:", bg='#2b2b2b', fg='white')
        label_arg.pack(side='left', padx=5)
        self.arg_var = tk.StringVar(value="30")
        arg_entry = ttk.Entry(add_frame, textvariable=self.arg_var, width=8)
        arg_entry.pack(side='left', padx=5)
        
        # Timeout
        label_timeout = tk.Label(add_frame, text="Timeout(s):", bg='#2b2b2b', fg='white')
        label_timeout.pack(side='left', padx=(20,5))
        self.timeout_var = tk.StringVar(value="60")
        timeout_spin = ttk.Spinbox(add_frame, from_=0, to=300, textvariable=self.timeout_var, width=6)
        timeout_spin.pack(side='left', padx=5)
        
        # Priority
        label_priority = tk.Label(add_frame, text="Priority:", bg='#2b2b2b', fg='white')
        label_priority.pack(side='left', padx=(10,5))
        self.priority_var = tk.IntVar(value=0)
        priority_spin = ttk.Spinbox(add_frame, from_=-10, to=10, textvariable=self.priority_var, width=5)
        priority_spin.pack(side='left', padx=5)
        
        # Add button
        add_btn = tk.Button(add_frame, text="➕ Add Task", bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'),
                           command=self.add_task, padx=10)
        add_btn.pack(side='left', padx=10)
        
        # Clear button
        clear_btn = tk.Button(add_frame, text="🗑️ Clear Done Tasks", bg="#f44336", fg="white", 
                            command=self.clear_completed, padx=10)
        clear_btn.pack(side='right', padx=(0,10))
        
        # Delete selected button
        delete_btn = tk.Button(add_frame, text="❌ Delete Selected", bg="#ff9800", fg="white",
                              command=self.delete_selected, padx=10)
        delete_btn.pack(side='right')
    
    def add_task(self):
        """Add new task based on UI inputs (10 types)."""
        try:
            task_type = self.task_var.get()
            arg = float(self.arg_var.get())
            timeout = int(self.timeout_var.get()) if self.timeout_var.get() else None
            priority = self.priority_var.get()
            
            from task import fibonacci, sleep_print, error_task, matrix_multiply, prime_check, string_reverse, json_parse, file_simulate, math_sum, sort_list
            
            if task_type == "fibonacci":
                self.pool.add_task(fibonacci, arg, priority=priority, timeout=timeout)
            elif task_type == "sleep_print":
                self.pool.add_task(sleep_print, arg, "Demo", priority=priority, timeout=timeout)
            elif task_type == "error_task":
                self.pool.add_task(error_task, priority=priority, timeout=timeout)
            elif task_type == "matrix_multiply":
                self.pool.add_task(matrix_multiply, int(arg), priority=priority, timeout=timeout)
            elif task_type == "prime_check":
                self.pool.add_task(prime_check, int(arg), priority=priority, timeout=timeout)
            elif task_type == "string_reverse":
                self.pool.add_task(string_reverse, f"Text{int(arg)}", priority=priority, timeout=timeout)
            elif task_type == "json_parse":
                self.pool.add_task(json_parse, int(arg), priority=priority, timeout=timeout)
            elif task_type == "file_simulate":
                self.pool.add_task(file_simulate, "demo.txt", int(arg), priority=priority, timeout=timeout)
            elif task_type == "math_sum":
                self.pool.add_task(math_sum, int(arg), priority=priority, timeout=timeout)
            elif task_type == "sort_list":
                self.pool.add_task(sort_list, int(arg), priority=priority, timeout=timeout)
            
            messagebox.showinfo("Success", f"Added {task_type}! Arg: {arg}, Priority: {priority}")
        except ValueError:
            messagebox.showerror("Error", "Arg must be number for most tasks.")
    
    def clear_completed(self):
        """Clear completed tasks from backend."""
        self.pool.clear_completed()
        self.update_tasks()
    
    def update_loop(self):
        """Periodic UI update."""
        self.update_stats()
        self.update_tasks()
        self.root.after(2000, self.update_loop)  # Update every 2s to prevent deselect during 1s update
    
    def update_stats(self):
        """Update stats labels."""
        stats = self.pool.get_stats()
        for key, label in self.stats_labels.items():
            value = stats.get(key, 0)
            label.config(text=f"{key.replace('_', ' ').title()}: {value}")
    
    def delete_selected(self):
        """Delete selected task from treeview."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a task to delete.")
            return
        
        full_id = self.tree.item(selection[0])['values'][0]  # Short ID from UI
        # Find full ID matching prefix
        tasks = self.pool.get_all_tasks()
        matching_tasks = [t for t in tasks if t['id'].startswith(full_id)]
        if not matching_tasks:
            messagebox.showwarning("Not Found", f"No task with ID starting {full_id}")
            self.update_tasks()
            return
        task_id = matching_tasks[0]['id']
        if messagebox.askyesno("Confirm", f"Delete task {task_id}?"):
            removed = self.pool.remove_task(task_id)
            status = "Success" if removed else "Failed (already gone)"
            messagebox.showinfo(status, f"Task {task_id}: {status}")
        self.update_tasks()

    def update_tasks(self):
        """Update tasks treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        tasks = self.pool.get_all_tasks()
        for task in sorted(tasks, key=lambda t: t.get('priority', 0)):
            values = (
                task['id'][:8],
                task['status'],
                task['priority'],
                f"{task.get('timeout', 'unlimited')}s",
                task['func'].__name__,
                f"{task['elapsed_time']:.1f}s",
                (str(task.get('result', 'N/A'))[:25] + "..." if task.get('result') is not None else 
                 str(task.get('error', 'No error'))[:25] + "...")
            )
            self.tree.insert('', 'end', values=values)
    
    def run(self):
        """Start the UI."""
        # Add sample tasks on startup
        self.pool.add_task(fibonacci, 28, priority=5, timeout=60)
        self.pool.add_task(sleep_print, 3.0, "Sample IO task", priority=1, timeout=10)
        self.root.mainloop()

if __name__ == "__main__":
    pool = ThreadPool(4)
    ui = ThreadPoolUI(pool)
    try:
        ui.run()
    finally:
        pool.shutdown()

