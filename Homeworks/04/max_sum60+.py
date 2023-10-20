# Check whether the current sum is less than the what already computed

# pro dalsi indexy ktere maji stejny prvek zkusim protahnout zdali to matchuje a pak teprv resit sumy a tak


# Get input from the user
input_str = input()
# input_str = "1 2 5 -6 8 -3 2 1 1 2 2 5 -6 8 -3 2 3"

# Convert the input string into a list of integers
input_list = list(map(int, input_str.split()))


# Function to check if a subarray is present in the array
def is_subarray(arr, subarray):
    if len(arr) < len(subarray):
        return False

    # Iterate through possible starting indices of subarray in arr
    for i in range(len(arr) - len(subarray) + 1):
        # Check if the subarray starting from index i matches the target subarray
        match = all(arr[i + j] == subarray[j] for j in range(len(subarray)))

        if match:
            return True

    return False


# Convert input_list to a set for faster membership testing
input_set = set(input_list)

# List to store found subarrays
temp = []

# Set to store unique subarrays for efficient membership testing
subarray_set = set()

# Iterate over each element in input_list
for i in range(len(input_list)):
    temp_j = []  # Temporary list to store subarrays starting from index i

    # Iterate over elements from i+1 to the end of the list
    for j in range(i + 1, len(input_list)):
        # Create a tuple representing the current subarray for set membership testing
        subarray = tuple(input_list[i:j])

        # Check if the current subarray is already in the set
        if is_subarray(input_list[j:], input_list[i:j]):
            temp_j.append(subarray)
        # If the subarray is not in the input_set and temp_j is not empty, exit the loop
        elif subarray not in input_set and temp_j:
            break

    # Extend the temp list with the found subarrays
    temp.extend(temp_j)

    # Update the set with the new subarrays
    subarray_set.update(temp_j)

# Initialize variables to store the final result
final_sum = sum(temp[0])
final_length = len(temp[0])

# Iterate over found subarrays to find the one with the maximum sum
for subarray in temp:
    current_sum = sum(subarray)
    if current_sum > final_sum:
        final_sum = current_sum
        final_length = len(subarray)

# Print the final result
print(final_length, final_sum)
