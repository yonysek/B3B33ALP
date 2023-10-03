# nums = list(map(int, input().split()))
nums = list(map(int, "-2 -3 4 -1 -2 1 5".split()))


# cur_length = 0
# cur_sum = 0

# first_try = True

# for i in range(len(nums)):
#   for j in range(i + 1,len(nums) + 1):
#     for k in range(len(nums[i:j])):
#       cur_sum += nums[i:j][k]
#       cur_length = len(nums[i:j])


#     if first_try or cur_sum > highest_sum:
#         highest_sum = cur_sum
#         highest_length = cur_length
#         first_try = False
#     cur_sum = 0
#     cur_length = 0

# print(highest_sum, highest_length)


cur_sum = nums[0]
highest_sum = nums[0]
end_index = 0

for i in range(1, len(nums)):
    cur_sum = max(nums[i], cur_sum + nums[i])

    if cur_sum > highest_sum:
        highest_sum = cur_sum
        end_index = i

start_index = end_index

decrement = highest_sum

while start_index >= 0:
    decrement -= nums[start_index]

    if decrement == 0:
        break

    start_index -= 1


highest_length = (end_index + 1) - start_index


print(highest_length, highest_sum)
