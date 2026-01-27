import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f4f8")
        
        self.data = []
        self.sorted_data = []
        
        title_frame = tk.Frame(root, bg="#2563eb", pady=20)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text="🔽 SORTING ALGORITHM VISUALIZER", 
                              font=("Arial", 24, "bold"), bg="#2563eb", fg="white")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Choose your algorithm and sort data in descending order", 
                                 font=("Arial", 11), bg="#2563eb", fg="#dbeafe")
        subtitle_label.pack()
        
        control_frame = tk.Frame(root, bg="#f0f4f8", pady=20)
        control_frame.pack(fill=tk.X, padx=20)
        
        file_frame = tk.LabelFrame(control_frame, text="  Upload Dataset  ", 
                                  font=("Arial", 10, "bold"), bg="#f0f4f8", fg="#1e40af", padx=10, pady=10)
        file_frame.grid(row=0, column=0, padx=10, sticky="ew")
        
        self.upload_btn = tk.Button(file_frame, text="📁 Choose File", 
                                   command=self.load_file, font=("Arial", 10, "bold"),
                                   bg="#3b82f6", fg="white", cursor="hand2", padx=20, pady=8)
        self.upload_btn.pack()
        
        self.file_status = tk.Label(file_frame, text="No file loaded", 
                                   font=("Arial", 9), bg="#f0f4f8", fg="#6b7280")
        self.file_status.pack(pady=5)
        
        algo_frame = tk.LabelFrame(control_frame, text="  Sorting Algorithm  ", 
                                  font=("Arial", 10, "bold"), bg="#f0f4f8", fg="#1e40af", padx=10, pady=10)
        algo_frame.grid(row=0, column=1, padx=10, sticky="ew")
        
        self.algo_var = tk.StringVar(value="bubble")
        algorithms = [("Bubble Sort", "bubble"), ("Selection Sort", "selection"), 
                     ("Insertion Sort", "insertion"), ("Quick Sort", "quick"), 
                     ("Merge Sort", "merge")]
        
        for text, value in algorithms:
            tk.Radiobutton(algo_frame, text=text, variable=self.algo_var, value=value,
                         font=("Arial", 9), bg="#f0f4f8", fg="#374151", 
                         selectcolor="#dbeafe", cursor="hand2").pack(anchor=tk.W)
        
        action_frame = tk.LabelFrame(control_frame, text="  Actions  ", 
                                    font=("Arial", 10, "bold"), bg="#f0f4f8", fg="#1e40af", padx=10, pady=10)
        action_frame.grid(row=0, column=2, padx=10, sticky="ew")
        
        self.sort_btn = tk.Button(action_frame, text="▶ Sort", command=self.sort_data,
                                 font=("Arial", 11, "bold"), bg="#16a34a", fg="white",
                                 cursor="hand2", padx=30, pady=10, state=tk.DISABLED)
        self.sort_btn.pack(pady=5)
        
        self.reset_btn = tk.Button(action_frame, text="🔄 Reset", command=self.reset_data,
                                  font=("Arial", 10, "bold"), bg="#6b7280", fg="white",
                                  cursor="hand2", padx=30, pady=8, state=tk.DISABLED)
        self.reset_btn.pack(pady=5)
        
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)
        
        self.result_frame = tk.Frame(root, bg="#f0f4f8")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        result_label = tk.Label(self.result_frame, text="DATA DISPLAY", 
                               font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#1e40af")
        result_label.pack(pady=5)
        
        text_frame = tk.Frame(self.result_frame, bg="white", relief=tk.SOLID, borderwidth=2)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(text_frame, font=("Courier", 10), wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set, bg="white", fg="#1f2937")
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.result_text.yview)
        
        self.result_text.insert(tk.END, "📤 Upload a dataset file to get started\n\n")
        self.result_text.insert(tk.END, "File should contain one number per line")
        self.result_text.config(state=tk.DISABLED)
    
    def load_file(self):
        filename = filedialog.askopenfilename(title="Select Dataset File",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.data = [int(line.strip()) for line in f if line.strip()]
                
                self.file_status.config(text=f"✓ {len(self.data)} elements loaded", fg="#16a34a")
                self.sort_btn.config(state=tk.NORMAL)
                self.sorted_data = []
                
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"📊 ORIGINAL DATA ({len(self.data)} elements)\n")
                self.result_text.insert(tk.END, "=" * 80 + "\n\n")
                self.result_text.insert(tk.END, f"First 20: {self.data[:20]}\n")
                self.result_text.insert(tk.END, f"Last 20: {self.data[-20:]}\n\n")
                self.result_text.insert(tk.END, "Click 'Sort' to sort the data in descending order")
                self.result_text.config(state=tk.DISABLED)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def sort_data(self):
        if not self.data:
            return
        
        self.sort_btn.config(state=tk.DISABLED, text="Sorting...")
        self.root.update()
        
        arr = self.data.copy()
        algorithm = self.algo_var.get()
        start_time = time.time()
        
        if algorithm == "bubble":
            n = len(arr)
            for i in range(n):
                swapped = False
                for j in range(0, n - i - 1):
                    if arr[j] < arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        swapped = True
                if not swapped:
                    break
        
        elif algorithm == "selection":
            n = len(arr)
            for i in range(n - 1):
                max_idx = i
                for j in range(i + 1, n):
                    if arr[j] > arr[max_idx]:
                        max_idx = j
                if max_idx != i:
                    arr[i], arr[max_idx] = arr[max_idx], arr[i]
        
        elif algorithm == "insertion":
            n = len(arr)
            for i in range(1, n):
                key = arr[i]
                j = i - 1
                while j >= 0 and arr[j] < key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        
        elif algorithm == "quick":
            stack = [(0, len(arr) - 1)]
            while stack:
                low, high = stack.pop()
                if low < high:
                    pivot = arr[high]
                    i = low - 1
                    for j in range(low, high):
                        if arr[j] > pivot:
                            i += 1
                            arr[i], arr[j] = arr[j], arr[i]
                    arr[i + 1], arr[high] = arr[high], arr[i + 1]
                    pi = i + 1
                    stack.append((low, pi - 1))
                    stack.append((pi + 1, high))
        
        elif algorithm == "merge":
            width = 1
            n = len(arr)
            while width < n:
                for i in range(0, n, width * 2):
                    left = i
                    mid = min(i + width, n)
                    right = min(i + width * 2, n)
                    L = arr[left:mid]
                    R = arr[mid:right]
                    l_idx = r_idx = 0
                    k = left
                    while l_idx < len(L) and r_idx < len(R):
                        if L[l_idx] >= R[r_idx]:
                            arr[k] = L[l_idx]
                            l_idx += 1
                        else:
                            arr[k] = R[r_idx]
                            r_idx += 1
                        k += 1
                    while l_idx < len(L):
                        arr[k] = L[l_idx]
                        l_idx += 1
                        k += 1
                    while r_idx < len(R):
                        arr[k] = R[r_idx]
                        r_idx += 1
                        k += 1
                width *= 2
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        self.sorted_data = arr
        
        algo_names = {"bubble": "Bubble Sort", "selection": "Selection Sort", 
                     "insertion": "Insertion Sort", "quick": "Quick Sort", "merge": "Merge Sort"}
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "✓ SORTING COMPLETE\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n\n")
        self.result_text.insert(tk.END, f"Algorithm: {algo_names[algorithm]}\n")
        self.result_text.insert(tk.END, f"Elements: {len(arr)}\n")
        self.result_text.insert(tk.END, f"Time: {time_taken:.6f} seconds\n")
        self.result_text.insert(tk.END, f"Order: Descending (Largest to Smallest)\n\n")
        self.result_text.insert(tk.END, "SORTED DATA:\n")
        self.result_text.insert(tk.END, "-" * 80 + "\n")
        
        for i, val in enumerate(arr):
            self.result_text.insert(tk.END, f"{val:6} ")
            if (i + 1) % 10 == 0:
                self.result_text.insert(tk.END, "\n")
        
        self.result_text.insert(tk.END, "\n" + "-" * 80)
        self.result_text.config(state=tk.DISABLED)
        
        self.sort_btn.config(state=tk.NORMAL, text="▶ Sort")
        self.reset_btn.config(state=tk.NORMAL)
    
    def reset_data(self):
        self.sorted_data = []
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"📊 ORIGINAL DATA ({len(self.data)} elements)\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n\n")
        self.result_text.insert(tk.END, f"First 20: {self.data[:20]}\n")
        self.result_text.insert(tk.END, f"Last 20: {self.data[-20:]}\n\n")
        self.result_text.insert(tk.END, "Click 'Sort' to sort the data in descending order")
        self.result_text.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()