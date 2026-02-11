#!/usr/bin/env python3
"""
SORTING ALGORITHM BENCHMARK TOOL - STANDALONE GUI VERSION
Features: 
- Real-time Progress Bar (%) & Cancel Option
- Save FULL sorted results to .txt
- Session History & Search Functionality
- Automatic 'generated_data.csv' detection
- Fully editable 'Rows to Load' field
"""

import csv
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path
import threading
from datetime import datetime

# ============================================================================
# SORTING ALGORITHMS (Updated with Progress Tracking & Cancellation)
# ============================================================================

def bubble_sort(data, key_func, progress_callback, stop_event):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        if stop_event.is_set(): return None
        # Update progress every iteration of the outer loop
        progress_callback(int((i / n) * 100))
        
        swapped = False
        for j in range(0, n - i - 1):
            if key_func(arr[j]) > key_func(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped: break
    return arr

def insertion_sort(data, key_func, progress_callback, stop_event):
    arr = data.copy()
    n = len(arr)
    for i in range(1, n):
        if stop_event.is_set(): return None
        # Update progress periodically to keep GUI responsive
        if i % (max(1, n // 100)) == 0:
            progress_callback(int((i / n) * 100))
            
        key_item = arr[i]
        key_value = key_func(key_item)
        j = i - 1
        while j >= 0 and key_func(arr[j]) > key_value:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

def merge_sort(data, key_func, progress_callback, stop_event):
    arr = data.copy()
    if len(arr) <= 1: return arr
    
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if stop_event.is_set(): return []
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:]); result.extend(right[j:])
        return result

    def msort(a, depth=0):
        if stop_event.is_set() or len(a) <= 1: return a
        # Merge sort is fast, so we simulate progress based on recursion depth
        if depth < 10: progress_callback(depth * 10)
        mid = len(a) // 2
        return merge(msort(a[:mid], depth+1), msort(a[mid:], depth+1))
    
    res = msort(arr)
    progress_callback(100)
    return res

# ============================================================================
# GUI APPLICATION
# ============================================================================

class BenchmarkGUI:
    def __init__(self, root):
        self.root = root
        self.csv_path = None
        self.data = []
        self.history = []
        self.last_sorted_result = None
        self.stop_event = threading.Event()
        
        self.setup_window()
        self.create_widgets()
        self.prompt_csv_file() # Original logic to detect file in folder
    
    def setup_window(self):
        self.root.title("Sorting Algorithm Benchmark Tool")
        self.root.geometry("1100x800")
        self.root.configure(bg='#f0f2f5')

    def add_history(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"[{timestamp}] {msg}")

    def prompt_csv_file(self):
        """Original feature: Detect if generated_data.csv exists"""
        default_path = Path("generated_data.csv")
        if default_path.exists():
            if messagebox.askyesno("File Found", "Use 'generated_data.csv' found in folder?"):
                self.csv_path = default_path
                return
        
        file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if file_path: self.csv_path = Path(file_path)

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=70)
        header.pack(fill='x')
        tk.Label(header, text="Sorting Algorithm Benchmark Tool", font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50').pack(pady=15)

        main_frame = tk.Frame(self.root, bg='#f0f2f5')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Left Panel (Controls)
        left_panel = tk.Frame(main_frame, width=320, bg='white', relief='ridge', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 15))

        # 1. Loading Section
        f1 = tk.LabelFrame(left_panel, text=" 1. Load Data ", bg='white', font=('Arial', 10, 'bold'))
        f1.pack(fill='x', padx=10, pady=10)
        self.rows_var = tk.StringVar(value="5000")
        self.rows_entry = tk.Entry(f1, textvariable=self.rows_var, font=('Arial', 11))
        self.rows_entry.pack(fill='x', padx=10, pady=5)
        tk.Button(f1, text="LOAD DATA", command=self.load_data, bg='#3498db', fg='white').pack(fill='x', padx=10, pady=5)
        self.data_status = tk.Label(f1, text="No data loaded", fg='red', bg='white')
        self.data_status.pack()

        # 2. Sort Section
        f2 = tk.LabelFrame(left_panel, text=" 2. Sort Settings ", bg='white', font=('Arial', 10, 'bold'))
        f2.pack(fill='x', padx=10, pady=5)
        self.algo_var = tk.StringVar(value="merge")
        for t, v in [("Bubble Sort", "bubble"), ("Insertion Sort", "insertion"), ("Merge Sort", "merge")]:
            tk.Radiobutton(f2, text=t, variable=self.algo_var, value=v, bg='white').pack(anchor='w', padx=5)
        
        self.col_var = tk.StringVar(value="ID")
        tk.OptionMenu(f2, self.col_var, "ID", "FirstName", "LastName").pack(fill='x', padx=10, pady=5)
        
        self.run_btn = tk.Button(f2, text="▶ RUN SORT", command=self.run_benchmark, bg='#27ae60', fg='white', font=('Arial', 11, 'bold'))
        self.run_btn.pack(fill='x', padx=10, pady=10)
        
        self.cancel_btn = tk.Button(f2, text="🛑 CANCEL SORT", command=self.cancel_sort, bg='#e74c3c', fg='white', state='disabled')
        self.cancel_btn.pack(fill='x', padx=10, pady=5)

        # 3. Features
        f3 = tk.LabelFrame(left_panel, text=" 3. Search & History ", bg='white', font=('Arial', 10, 'bold'))
        f3.pack(fill='x', padx=10, pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(f3, textvariable=self.search_var).pack(fill='x', padx=10, pady=5)
        tk.Button(f3, text="Search in Data", command=self.perform_search).pack(fill='x', padx=10, pady=2)
        tk.Button(left_panel, text="View Session History", command=self.show_history).pack(fill='x', padx=10, pady=10)
        tk.Button(left_panel, text="Clear Results", command=self.clear_results, bg='#95a5a6', fg='white').pack(fill='x', padx=10)

        # Right Panel (Output)
        right_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)

        toolbar = tk.Frame(right_panel, bg='#ecf0f1')
        toolbar.pack(fill='x')
        tk.Label(toolbar, text="Output Terminal", font=('Arial', 10, 'bold'), bg='#ecf0f1').pack(side='left', padx=10)
        
        # RESTORED: SAVE TO FILE BUTTON
        self.save_btn = tk.Button(toolbar, text="💾 SAVE FULL LIST TO TXT", command=self.save_to_txt, state='disabled', bg='#e67e22', fg='white', font=('Arial', 9, 'bold'))
        self.save_btn.pack(side='right', padx=10, pady=5)

        # Progress Labels
        self.prog_info = tk.Frame(right_panel, bg='white')
        self.prog_info.pack(fill='x', padx=10, pady=(10, 0))
        self.prog_label = tk.Label(self.prog_info, text="System Idle", bg='white', font=('Arial', 9, 'italic'))
        self.prog_label.pack(side='left')
        self.pct_label = tk.Label(self.prog_info, text="0%", bg='white', font=('Arial', 9, 'bold'))
        self.pct_label.pack(side='right')

        self.prog_bar = ttk.Progressbar(right_panel, mode='determinate')
        self.prog_bar.pack(fill='x', padx=10, pady=(0, 10))

        self.results_text = scrolledtext.ScrolledText(right_panel, font=('Consolas', 10), state='disabled', bg='#1e1e1e', fg='#d4d4d4')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)

    # ============================================================================
    # LOGIC METHODS
    # ============================================================================

    def load_data(self):
        if not self.csv_path: return messagebox.showerror("Error", "No CSV file selected.")
        try:
            num = int(self.rows_var.get())
            self.data = []
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= num: break
                    self.data.append({k.replace('\ufeff', ''): v.strip() for k, v in row.items()})
            self.data_status.config(text=f"✓ {len(self.data):,} rows loaded", fg='green')
            self.log(f"Loaded {len(self.data):,} rows from {self.csv_path.name}")
            self.add_history(f"Loaded {len(self.data)} rows.")
        except Exception as e:
            messagebox.showerror("Error", f"Check row count: {e}")

    def run_benchmark(self):
        if not self.data: return messagebox.showwarning("Warning", "Load data first!")
        self.stop_event.clear()
        self.save_btn.config(state='disabled')
        self.run_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.prog_bar['value'] = 0
        
        algo = self.algo_var.get()
        col = self.col_var.get()
        threading.Thread(target=self._worker, args=(algo, col), daemon=True).start()

    def _worker(self, algo_key, col_key):
        self.root.after(0, self.prog_label.config, {"text": f"Sorting with {algo_key}..."})
        key_func = lambda r: int(r['ID']) if col_key == 'ID' else r[col_key].lower()
        algo_func = {'bubble': bubble_sort, 'insertion': insertion_sort, 'merge': merge_sort}[algo_key]
        
        start_time = time.perf_counter()
        sorted_data = algo_func(self.data, key_func, self._update_prog_ui, self.stop_event)
        duration = time.perf_counter() - start_time
        
        if self.stop_event.is_set():
            self.root.after(0, self.log, "❌ Sort cancelled by user.")
        else:
            self.last_sorted_result = {'data': sorted_data, 'algo': algo_key, 'col': col_key, 'time': duration}
            self.root.after(0, self._finish_ui)
        
        self.root.after(0, self._reset_ui)

    def _update_prog_ui(self, val):
        self.root.after(0, self._set_bar, val)

    def _set_bar(self, val):
        self.prog_bar['value'] = val
        self.pct_label.config(text=f"{val}%")

    def _finish_ui(self):
        res = self.last_sorted_result
        self.save_btn.config(state='normal')
        self.log(f"\n✨ SORT COMPLETE: {res['algo'].upper()}\nTime: {res['time']:.4f}s | Column: {res['col']}\nPreview (Top 5):")
        for row in res['data'][:5]:
            self.log(f"-> {row['ID']} | {row['FirstName']} {row['LastName']}")
        self.add_history(f"Sorted {len(res['data'])} rows in {res['time']:.2f}s")

    def _reset_ui(self):
        self.run_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        self.prog_label.config(text="System Idle")

    def cancel_sort(self):
        self.stop_event.set()
        self.cancel_btn.config(state='disabled')

    def save_to_txt(self):
        """Restored: Saves every sorted row to a text file"""
        if not self.last_sorted_result: return
        res = self.last_sorted_result
        filename = f"sorted_{res['algo']}_{res['col']}.txt"
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename)
        
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(f"SORTED DATA EXPORT - {res['algo'].upper()}\n")
                    f.write(f"Column: {res['col']} | Rows: {len(res['data'])}\n" + "="*50 + "\n")
                    for r in res['data']:
                        f.write(f"{r['ID']:<10} {r['FirstName']:<20} {r['LastName']}\n")
                messagebox.showinfo("Saved", f"Results exported to {Path(path).name}")
                self.add_history(f"Exported data to {Path(path).name}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def perform_search(self):
        term = self.search_var.get().lower()
        if not self.data or not term: return
        results = [r for r in self.data if term in str(r.values()).lower()]
        self.log(f"\n🔍 Search for '{term}': Found {len(results)} matches.")
        for r in results[:5]: self.log(f"-> {r['ID']} | {r['FirstName']} {r['LastName']}")

    def show_history(self):
        h_win = tk.Toplevel(self.root)
        h_win.title("Session History")
        txt = scrolledtext.ScrolledText(h_win, width=60, height=20)
        txt.pack(padx=10, pady=10)
        txt.insert(tk.END, "\n".join(self.history) if self.history else "No history yet.")
        txt.config(state='disabled')

    def log(self, text):
        self.results_text.config(state='normal')
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state='disabled')

    def clear_results(self):
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.prog_bar['value'] = 0
        self.pct_label.config(text="0%")
        messagebox.showinfo("Reset", "Display cleared.")

if __name__ == "__main__":
    root = tk.Tk()
    BenchmarkGUI(root)
    root.mainloop()