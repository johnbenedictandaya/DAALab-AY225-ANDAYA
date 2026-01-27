# DAALab-AY225
The DAA-Lab Repo

# Sorting Applications Analysis

## Overview
You have created **three different Python applications** for sorting data in **descending order**. Each serves a different purpose and has unique features. All three applications use the same dataset (`dataset.txt`) which contains 19,998 numbers ranging from 1 to 9998 in a shuffled order.

---

## 1. **sorting_app.py** - GUI Desktop Application

### Purpose
A professional desktop application with a graphical user interface (GUI) built using Tkinter.

### Key Features
- **Modern UI Design**: Blue color scheme with professional styling
- **File Upload**: Browse and select any text file containing numbers
- **5 Sorting Algorithms**:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Quick Sort
  - Merge Sort
- **Visual Display**: Shows sorted results in a scrollable text area
- **Performance Metrics**: Displays time taken for sorting
- **Reset Function**: Return to original data view

### When to Use
- When you want a user-friendly interface
- For demonstrations or presentations
- When you prefer clicking buttons over typing commands
- For users unfamiliar with command-line interfaces

### How to Run
```bash
python sorting_app.py
```

### Workflow
1. Launch the application → GUI window opens
2. Click "Choose File" → Select your dataset
3. Select a sorting algorithm (radio buttons)
4. Click "Sort" → View results
5. Click "Reset" to see original data again

---

## 2. **sorting_appterm.py** - Terminal-Based Interactive Application

### Purpose
A command-line application with an interactive menu system and clear visual formatting.

### Key Features
- **Menu-Driven Interface**: Easy-to-navigate text menus
- **Same 5 Algorithms**: Bubble, Selection, Insertion, Quick, Merge Sort
- **Screen Clearing**: Cleans terminal for better readability
- **Detailed Results**: Shows all sorted data with formatting
- **Verification Check**: Confirms sorting was successful
- **Continuous Operation**: Sort multiple times with different algorithms without restarting
- **Professional Formatting**: Uses separators and clear sections

### When to Use
- When running on servers without GUI support
- For quick testing via terminal/command prompt
- When you want a clean, focused interface
- For users comfortable with command-line tools

### How to Run
```bash
python sorting_appterm.py
```

### Workflow
1. Run the script → Prompts for dataset file path
2. Press Enter to use default "dataset.txt"
3. View menu → Select algorithm (1-5)
4. View sorted results
5. Choose to sort again with different algorithm or exit

---

## 3. **Sortingsystem.py** - Modular Library & Program

### Purpose
A reusable Python module that can work as both a standalone program and imported library.

### Key Features
- **Modular Functions**: Each sorting algorithm is a separate function
- **Return Time & Data**: Functions return both sorted data and execution time
- **3 Core Algorithms**: Bubble Sort, Insertion Sort, Merge Sort
- **Algorithm Comparison**: Option to compare performance of all algorithms
- **Flexible Data Reading**: Handles multiple number formats (integers, floats, comma/space separated)
- **Library-Ready**: Can be imported into other Python scripts

### When to Use
- When you want to integrate sorting into other Python projects
- For performance testing and algorithm comparison
- When you need reusable sorting functions
- For educational purposes to study algorithm implementation

### How to Run
**As standalone:**
```bash
python Sortingsystem.py
```

**As imported library:**
```python
from Sortingsystem import bubble_sort_descending, read_dataset
data = read_dataset("dataset.txt")
sorted_data, time_taken = bubble_sort_descending(data)
```

### Workflow
1. Run the script → Automatically loads "dataset.txt"
2. View menu → Choose option (1-5)
3. Options include:
   - Sort with individual algorithms
   - **Compare all sorting times** (unique feature!)
   - View sorted results
4. Loop until you choose to exit

---

## Comparison Table

| Feature | sorting_app.py | sorting_appterm.py | Sortingsystem.py |
|---------|----------------|-------------------|------------------|
| **Interface** | GUI (Tkinter) | Terminal Menu | Terminal Menu |
| **Algorithms** | 5 (Bubble, Selection, Insertion, Quick, Merge) | 5 (Same) | 3 (Bubble, Insertion, Merge) |
| **File Selection** | Browse button | Type path | Fixed filename |
| **Display Style** | Scrollable text box | Terminal output | Terminal output |
| **Comparison Mode** | ❌ No | ❌ No | ✅ Yes |
| **Reusable Code** | ❌ No | ❌ No | ✅ Yes (can import) |
| **Verification** | ❌ No | ✅ Yes | ✅ Yes |
| **Best For** | Presentations, non-tech users | Quick terminal use | Development, testing |

---

## Algorithm Details

All applications sort in **DESCENDING order** (largest to smallest).

### Implemented Algorithms

1. **Bubble Sort**
   - Compares adjacent elements and swaps them
   - Time Complexity: O(n²)
   - Good for: Small datasets, educational purposes

2. **Selection Sort**
   - Finds maximum element and places it at the beginning
   - Time Complexity: O(n²)
   - Good for: Small datasets, minimal swaps needed

3. **Insertion Sort**
   - Builds sorted array one element at a time
   - Time Complexity: O(n²)
   - Good for: Nearly sorted data, small datasets

4. **Quick Sort** (sorting_app.py & sorting_appterm.py only)
   - Divide-and-conquer using pivot
   - Time Complexity: O(n log n) average
   - Good for: Large datasets, general purpose

5. **Merge Sort**
   - Divide-and-conquer with merging
   - Time Complexity: O(n log n)
   - Good for: Large datasets, stable sorting needed

---

## Your Dataset

**File**: `dataset.txt`
- **Total numbers**: 19,998
- **Range**: 1 to 9998
- **Order**: Randomly shuffled
- **Format**: One number per line

When sorted in descending order, the result should be:
```
9998, 9997, 9996, ..., 3, 2, 1
```

---

## Recommendations

### For Different Use Cases:

1. **Demonstrating to non-technical users**
   - Use: `sorting_app.py`
   - Reason: Easy to use, visually appealing

2. **Quick testing on server**
   - Use: `sorting_appterm.py`
   - Reason: No GUI needed, clean interface

3. **Comparing algorithm performance**
   - Use: `Sortingsystem.py`
   - Reason: Built-in comparison feature

4. **Integrating into another project**
   - Use: `Sortingsystem.py` as import
   - Reason: Modular, reusable functions

5. **Learning algorithm implementation**
   - Study: All three
   - Reason: Different implementation styles

---

## Potential Improvements

### For sorting_app.py:
- Add export functionality (save sorted data to file)
- Add algorithm comparison feature
- Add progress bar for large datasets
- Add data visualization (charts/graphs)

### For sorting_appterm.py:
- Add file save option
- Add color coding for better readability
- Add progress indicators for large datasets

### For Sortingsystem.py:
- Add Quick Sort and Selection Sort
- Add graph generation for time comparisons
- Add option to change dataset filename
- Create a config file for settings

---

## Technical Notes

### Common Implementation Details:
- All use descending order: `arr[j] < arr[j+1]` or `arr[j] > arr[max_idx]`
- All measure execution time using `time.time()`
- All handle the same dataset format
- All copy data before sorting (preserves original)

### Performance Expectations (for 19,998 elements):
- **Bubble Sort**: ~10-30 seconds
- **Selection Sort**: ~8-20 seconds
- **Insertion Sort**: ~5-15 seconds
- **Quick Sort**: <1 second
- **Merge Sort**: <1 second

*Note: Actual times depend on your computer's specifications*

---

## Conclusion

You have three well-structured sorting applications, each suited for different scenarios:
- **sorting_app.py**: Best for user experience
- **sorting_appterm.py**: Best for terminal efficiency
- **Sortingsystem.py**: Best for development and testing

All applications successfully implement multiple sorting algorithms in descending order and provide timing information for performance analysis.