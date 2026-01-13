import time
import os

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 80)
    print(" " * 25 + "SORTING ALGORITHM SELECTOR")
    print("=" * 80)
    print()
    
    dataset_file = input("Enter the path to your dataset file (press Enter for 'dataset.txt'): ").strip()
    if not dataset_file:
        dataset_file = "dataset.txt"
    
    try:
        print(f"\n📂 Reading dataset from '{dataset_file}'...")
        with open(dataset_file, 'r') as f:
            data = [int(line.strip()) for line in f if line.strip()]
        
        print(f"✓ Dataset loaded successfully!")
        print(f"   Total elements: {len(data)}")
        print(f"   First 10: {data[:10]}")
        print(f"   Last 10: {data[-10:]}")
        print()
        input("Press Enter to continue...")
        
    except FileNotFoundError:
        print(f"\n✗ ERROR: File '{dataset_file}' not found.")
        print("   Please make sure the file exists in the correct location.")
        input("\nPress Enter to exit...")
        exit()
    except ValueError:
        print(f"\n✗ ERROR: File contains invalid data (non-numeric values).")
        input("\nPress Enter to exit...")
        exit()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        input("\nPress Enter to exit...")
        exit()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print(" " * 25 + "SORTING ALGORITHM SELECTOR")
        print("=" * 80)
        print(f"\nDataset: {dataset_file} ({len(data)} elements)")
        print()
        print("-" * 80)
        print("SELECT A SORTING ALGORITHM:")
        print("-" * 80)
        print()
        print("   1. Bubble Sort       - Simple comparison-based sorting")
        print("   2. Selection Sort    - Finds minimum/maximum iteratively")
        print("   3. Insertion Sort    - Builds sorted array one item at a time")
        print("   4. Quick Sort        - Efficient divide-and-conquer algorithm")
        print("   5. Merge Sort        - Stable divide-and-conquer algorithm")
        print()
        print("   6. Exit              - Close the program")
        print()
        print("-" * 80)
        
        choice = input("\n👉 Enter your choice (1-6): ").strip()
        
        if choice == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "=" * 80)
            print(" " * 25 + "Thank you for using the")
            print(" " * 22 + "SORTING ALGORITHM SELECTOR!")
            print("=" * 80)
            print()
            break
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("\n✗ Invalid choice! Please enter a number between 1 and 6.")
            input("\nPress Enter to try again...")
            continue
        
        arr = data.copy()
        algorithm_name = ""
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print(" " * 30 + "SORTING IN PROGRESS")
        print("=" * 80)
        print()
        
        start_time = time.time()
        
        if choice == '1':
            algorithm_name = "Bubble Sort"
            print(f"🔄 Running {algorithm_name}...")
            n = len(arr)
            for i in range(n - 1):
                swapped = False
                for j in range(0, n - i - 1):
                    if arr[j] < arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        swapped = True
                if not swapped:
                    break
        
        elif choice == '2':
            algorithm_name = "Selection Sort"
            print(f"🔄 Running {algorithm_name}...")
            n = len(arr)
            for i in range(n - 1):
                max_idx = i
                for j in range(i + 1, n):
                    if arr[j] > arr[max_idx]:
                        max_idx = j
                if max_idx != i:
                    arr[i], arr[max_idx] = arr[max_idx], arr[i]
        
        elif choice == '3':
            algorithm_name = "Insertion Sort"
            print(f"🔄 Running {algorithm_name}...")
            n = len(arr)
            for i in range(1, n):
                key = arr[i]
                j = i - 1
                while j >= 0 and arr[j] < key:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        
        elif choice == '4':
            algorithm_name = "Quick Sort"
            print(f"🔄 Running {algorithm_name}...")
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
        
        elif choice == '5':
            algorithm_name = "Merge Sort"
            print(f"🔄 Running {algorithm_name}...")
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
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print(" " * 32 + "✓ SORTING COMPLETE!")
        print("=" * 80)
        print()
        print(f"  Algorithm Used     : {algorithm_name}")
        print(f"  Total Elements     : {len(arr)}")
        print(f"  Time Taken         : {time_taken:.6f} seconds")
        print(f"  Sorting Order      : Descending (Largest → Smallest)")
        print()
        
        is_sorted = all(arr[i] >= arr[i+1] for i in range(len(arr)-1))
        status = "✓ YES" if is_sorted else "✗ NO"
        print(f"  Correctly Sorted   : {status}")
        print()
        print("=" * 80)
        print(" " * 33 + "SORTED DATA")
        print("=" * 80)
        print()
        
        for i, value in enumerate(arr, 1):
            print(f"{value:6}", end=" ")
            if i % 10 == 0:
                print()
        
        if len(arr) % 10 != 0:
            print()
        
        print()
        print("=" * 80)
        print()
        print(f"⏱️  TIME TAKEN: {time_taken:.6f} seconds")
        print()
        print("=" * 80)
        print()
        
        print("OPTIONS:")
        print("  1. Sort with a different algorithm")
        print("  2. Exit program")
        print()
        
        next_choice = input("👉 Enter your choice (1-2): ").strip()
        
        if next_choice != '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "=" * 80)
            print(" " * 25 + "Thank you for using the")
            print(" " * 22 + "SORTING ALGORITHM SELECTOR!")
            print("=" * 80)
            print()
            break