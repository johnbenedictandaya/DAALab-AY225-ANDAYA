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
   
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize by detecting if array is already sorted
        swapped = False
       
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is LESS than the next element (for descending)
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
       
        # If no swaps occurred, array is sorted
        if not swapped:
            break
   
    end_time = time.time()
    time_taken = end_time - start_time
   
    return arr, time_taken
 
 
def read_dataset(filename):
    """
    Reads numbers from a file and returns them as a list.
    Each number should be on a separate line or separated by spaces/commas.
   
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
                if line:  # Skip empty lines
                    try:
                        # Try to convert to int or float
                        if '.' in line:
                            numbers.append(float(line))
                        else:
                            numbers.append(int(line))
                    except ValueError:
                        # If a line contains multiple numbers separated by spaces or commas
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
 
 
# Main program
if __name__ == "__main__":
    filename = "dataset.txt"
    print(f"Reading data from '{filename}'...")
   
    data = read_dataset(filename)
   
    if data is not None:
        print(f"Dataset loaded: {len(data)} elements")
        print("Starting bubble sort (DESCENDING ORDER)...")
       
        sorted_data, time_taken = bubble_sort_descending(data.copy())
       
        print("SORTING COMPLETE!\n")
        print("Sorted elements (descending order):\n")
       
        # Print EVERY SINGLE element
        for i, num in enumerate(sorted_data, 1):
            print(f"{num}")
       
        print(f"\n==========================================")
        print(f"Time taken: {time_taken:.6f} seconds")
        print(f"Total elements sorted: {len(sorted_data)}")
       
        # Verify
        is_sorted = all(sorted_data[i] >= sorted_data[i+1] for i in range(len(sorted_data)-1))
        print(f"Verification: {'✓ CORRECT!' if is_sorted else '✗ FAILED!'}")
    else:
        print("Failed to read data.")