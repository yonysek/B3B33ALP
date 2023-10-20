# Input
# input_str = input()
# input_str = "3 3 3 3 3 3 3 3 3"
input_str = "1 2 3 3 3 3 3 3 3 3 3 3 4 5"
# input_str = "1 1 1 6 2 2 2 6 1 1 1"
# input_str = "1 2 3 4 1 2 3 4"
input = list(map(int, input_str.split()))


def arr_find(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


temp_arrs = []

for i in range(len(input)):
    arr_after = input[i + 1 :]

    if input[i] not in arr_after:
        continue
    temp_arrs.extend([[input[i]]])

    index = arr_find(arr_after, input[i])

    arr_after = arr_after[index + 1 :]

    delta = index - i + 2

    j = 1
    first_iter = True

    # We need to check if we are checking elements in the same array we are taking them from

    while True:
        if arr_after == []:
            break

        if input[i + j] != arr_after[0]:
            if not first_iter:
                break
            if input[i + j] not in arr_after[1:]:
                break

            index = arr_find(arr_after[1:], input[i + j])
            arr_after = arr_after[index + 1 :]
            # delta = index + 1 - i

        else:
            if len(input[i : +j + 1]) > len(input) / 2:
                break
            temp_arrs.extend([input[i : +j + 1]])

            arr_after = arr_after[1:]
            first_iter = False
            j += 1

        if i + j >= len(input):
            break


max_sum = sum(temp_arrs[0])
max_len = len(temp_arrs[0])
for i in range(len(temp_arrs)):
    if sum(temp_arrs[i]) > max_sum:
        max_sum = sum(temp_arrs[i])
        max_len = len(temp_arrs[i])


print(max_len, max_sum)
