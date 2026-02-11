#!/usr/bin/env python3
"""
ADVANCED SORTING BENCHMARK TOOL with SESSION HISTORY
"""

import csv
import time
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# SORTING ALGORITHMS WITH PROGRESS TRACKING
# ============================================================================

def print_progress_bar(iteration, total, prefix='', suffix='', length=40, fill='█'):
    """Terminal progress bar utility"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        print()

def bubble_sort(data, key_func):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        if i % (max(1, n // 100)) == 0 or i == n - 1:
            print_progress_bar(i + 1, n, prefix='Progress:', suffix='Complete', length=40)
        for j in range(0, n - i - 1):
            if key_func(arr[j]) > key_func(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            print_progress_bar(n, n, prefix='Progress:', suffix='Complete', length=40)
            break
    return arr

def insertion_sort(data, key_func):
    arr = data.copy()
    n = len(arr)
    for i in range(1, n):
        if i % (max(1, n // 100)) == 0 or i == n - 1:
            print_progress_bar(i + 1, n, prefix='Progress:', suffix='Complete', length=40)
        key_item = arr[i]
        key_value = key_func(key_item)
        j = i - 1
        while j >= 0 and key_func(arr[j]) > key_value:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

def merge_sort(data, key_func):
    arr = data.copy()
    if len(arr) <= 1: return arr
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:]); result.extend(right[j:])
        return result
    def msort(a):
        if len(a) <= 1: return a
        mid = len(a) // 2
        return merge(msort(a[:mid]), msort(a[mid:]))
    return msort(arr)

# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================

class BenchmarkApp:
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)
        self.data = []
        self.last_sorted = None
        self.history = [] # Stores execution history

    def add_to_history(self, action):
        """Timestamp and log an action"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"[{timestamp}] {action}")

    def load_data(self):
        print("\n📂 LOAD DATA")
        rows = input("Enter number of rows to load (Press Enter for ALL): ")
        limit = int(rows) if rows.isdigit() else None
        
        self.data = []
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if limit and i >= limit: break
                    clean_row = {k.replace('\ufeff', ''): v.strip() for k, v in row.items()}
                    self.data.append(clean_row)
            msg = f"Loaded {len(self.data):,} records from {self.csv_path.name}"
            print(f"✅ {msg}")
            self.add_to_history(msg)
        except Exception as e:
            print(f"❌ Error: {e}")

    def run_sort(self):
        if not self.data:
            print("❌ No data loaded.")
            return

        print("\nAlgorithms: 1. Bubble | 2. Insertion | 3. Merge")
        algo_choice = input("Choice: ")
        print("\nColumns: 1. ID | 2. FirstName | 3. LastName")
        col_choice = input("Choice: ")
        
        column = {'1': 'ID', '2': 'FirstName', '3': 'LastName'}.get(col_choice)
        algo_info = {'1': ('Bubble', bubble_sort), '2': ('Insertion', insertion_sort), '3': ('Merge', merge_sort)}.get(algo_choice)

        if algo_info and column:
            name, func = algo_info
            key_func = lambda r: int(r['ID']) if column == 'ID' else r[column].lower()
            
            print(f"\n🚀 Running {name} Sort on {column}...")
            start_time = time.perf_counter()
            self.last_sorted = func(self.data, key_func)
            duration = time.perf_counter() - start_time
            
            result_msg = f"Sorted {len(self.data):,} rows using {name} (Time: {duration:.4f}s)"
            print(f"✨ {result_msg}")
            self.add_to_history(result_msg)
            self.save_prompt()

    def show_history(self):
        """Displays the session log"""
        print("\n📜 EXECUTION HISTORY")
        print("-" * 50)
        if not self.history:
            print("No actions executed yet.")
        for entry in self.history:
            print(entry)
        print("-" * 50)

    def save_prompt(self):
        if input("\n💾 Save results to .txt? (y/n): ").lower() == 'y':
            fname = f"sorted_{int(time.time())}.txt"
            with open(fname, 'w') as f:
                for row in self.last_sorted:
                    f.write(f"{row['ID']}, {row['FirstName']}, {row['LastName']}\n")
            self.add_to_history(f"Saved results to {fname}")
            print(f"✅ Saved to {fname}")

    def menu(self):
        while True:
            print("\n1. Load Data | 2. Run Sort | 3. View History | 4. Exit")
            c = input("\nAction: ")
            if c == '1': self.load_data()
            elif c == '2': self.run_sort()
            elif c == '3': self.show_history()
            elif c == '4': break

if __name__ == "__main__":
    path = "generated_data.csv"
    if Path(path).exists():
        BenchmarkApp(path).menu()
    else:
        print(f"Error: {path} not found.")