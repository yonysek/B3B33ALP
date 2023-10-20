# While going through array check if the same array is already in the list, if not just skip to next element

# Input
# input = input()
input = "1 2 5 -6 8 -3 2 1 1 2 2 5 -6 8 -3 2 3"

input = list(map(int, input.split()))

# Function to tell if the subarray is in the array


def is_subarray(arr, subarray):
    if len(arr) < len(subarray):
        return False

    for i in range(len(arr) - len(subarray) + 1):
        match = all(arr[i + j] == subarray[j] for j in range(len(subarray)))

        if match:
            return True

    return False


temp = []

for i in range(len(input)):
    temp_j = []
    for j in range(i + 1, len(input)):
        if is_subarray(input[j:], input[i:j]):
            temp_j.append(input[i:j])
        elif input[i:j] not in input and temp_j != []:
            break
    temp.extend(temp_j)


final_sum = 0

final_length = len(temp[0])

for i in range(len(temp[0])):
    final_sum += int(temp[0][i])


for i in range(len(temp)):
    sum = 0
    for j in range(len(temp[i])):
        sum += int(temp[i][j])
    if sum > final_sum:
        final_sum = sum
        final_length = len(temp[i])


print(final_length, final_sum)
