import time

def bubble_sort_descending(arr):
    """
    Sorts an array in DESCENDING order using the bubble sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return arr, time_taken


def insertion_sort_descending(arr):
    """
    Sorts an array in DESCENDING order using the insertion sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements that are smaller than key to one position ahead
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return arr, time_taken


def merge_sort_descending(arr):
    """
    Sorts an array in DESCENDING order using the merge sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    
    def merge_sort_helper(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort_helper(arr[:mid])
        right = merge_sort_helper(arr[mid:])
        
        return merge(left, right)
    
    def merge(left, right):
        result = []
        i = j = 0
        
        # Merge in descending order
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    sorted_arr = merge_sort_helper(arr)
    end_time = time.time()
    time_taken = end_time - start_time
    
    return sorted_arr, time_taken


def read_dataset(filename):
    """
    Reads numbers from a file and returns them as a list.
    
    Args:
        filename: Path to the file containing numbers
        
    Returns:
        List of numbers read from the file
    """
    try:
        with open(filename, 'r') as file:
            numbers = []
            for line in file:
                line = line.strip()
                if line:
                    try:
                        if '.' in line:
                            numbers.append(float(line))
                        else:
                            numbers.append(int(line))
                    except ValueError:
                        if ',' in line:
                            nums = [float(x.strip()) if '.' in x.strip() else int(x.strip()) 
                                   for x in line.split(',') if x.strip()]
                            numbers.extend(nums)
                        else:
                            nums = [float(x.strip()) if '.' in x.strip() else int(x.strip()) 
                                   for x in line.split() if x.strip()]
                            numbers.extend(nums)
            
            return numbers
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def display_results(sorted_data, time_taken, algorithm_name):
    """
    Displays the sorting results in a formatted manner.
    
    Args:
        sorted_data: The sorted array
        time_taken: Time taken to sort in seconds
        algorithm_name: Name of the sorting algorithm used
    """
    print("\n" + "="*50)
    print(f"SORTING COMPLETE - {algorithm_name}")
    print("="*50)
    print("\nSorted elements (descending order):\n")
    
    for num in sorted_data:
        print(f"{num}")
    
    print(f"\n{'='*50}")
    print(f"Time taken: {time_taken:.6f} seconds")
    print(f"Total elements sorted: {len(sorted_data)}")
    
    is_sorted = all(sorted_data[i] >= sorted_data[i+1] for i in range(len(sorted_data)-1))
    print(f"Verification: {'✓ CORRECT!' if is_sorted else '✗ FAILED!'}")
    print("="*50 + "\n")


def display_menu():
    """
    Displays the main menu.
    """
    print("\n" + "="*50)
    print("     SORTING ALGORITHMS - DESCENDING ORDER")
    print("="*50)
    print("1. Bubble Sort")
    print("2. Insertion Sort")
    print("3. Merge Sort")
    print("4. Exit")
    print("="*50)


def main():
    """
    Main program loop.
    """
    filename = "dataset.txt"
    
    print("\n" + "*"*50)
    print("     WELCOME TO SORTING ALGORITHMS PROGRAM")
    print("*"*50)
    print(f"\nReading data from '{filename}'...")
    
    data = read_dataset(filename)
    
    if data is None:
        print("Failed to read data. Exiting program.")
        return
    
    print(f"✓ Dataset loaded successfully: {len(data)} elements")
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\n→ Running BUBBLE SORT...")
                sorted_data, time_taken = bubble_sort_descending(data.copy())
                display_results(sorted_data, time_taken, "BUBBLE SORT")
                
            elif choice == '2':
                print("\n→ Running INSERTION SORT...")
                sorted_data, time_taken = insertion_sort_descending(data.copy())
                display_results(sorted_data, time_taken, "INSERTION SORT")
                
            elif choice == '3':
                print("\n→ Running MERGE SORT...")
                sorted_data, time_taken = merge_sort_descending(data.copy())
                display_results(sorted_data, time_taken, "MERGE SORT")
                
            elif choice == '4':
                print("\n" + "*"*50)
                print("     Thank you for using the program!")
                print("     Exiting...")
                print("*"*50 + "\n")
                break
                
            else:
                print("\n⚠ Invalid choice! Please enter a number between 1 and 4.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\n⚠ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()