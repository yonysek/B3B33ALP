def max_sum_subarray(input_list):
    max_sum = float("-inf")  # Initialize max_sum to negative infinity
    current_sum = 0  # Initialize current_sum to zero
    start_index = 0  # Initialize start_index to zero

    for i in range(len(input_list)):
        current_sum += input_list[i]

        if current_sum > max_sum:
            max_sum = current_sum
            end_index = i

        if current_sum < 0:
            current_sum = 0
            start_index = i + 1

    return start_index, end_index, max_sum


# Get input from the user
# input_str = input()
input_str = "1 2 5 -6 8 -3 2 1 1 2 2 5 -6 8 -3 2 3"

input_list = list(map(int, input_str.split()))

# Find the maximum sum subarray in the entire array
start, end, maximum_sum = max_sum_subarray(input_list)

# Find the maximum sum subarray in the remaining array
_, _, second_max_sum = max_sum_subarray(input_list[end + 1 :])

# Print the result
print(
    end - start + 1 + len(input_list) * (second_max_sum > 0),
    maximum_sum + second_max_sum,
)
