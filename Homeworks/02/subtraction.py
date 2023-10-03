import math
from decimal import Decimal, getcontext

# Inputs
# num1 = input()
# num2 = input()

num1 = "1.11011e1101"
num2 = "1.001e-101"

nums = [num1, num2]


# Test what operation are we doing
forms_of_operation = ["n1-n2", "n2-n1", "n1+n2", "-(n1+n2)"]
types_of_operation = ["+", "-"]


def get_operation_type(nums):
    no_minus = False
    for i in range(len(nums)):
        if nums[i][0] != "-":
            no_minus = True
        else:
            no_minus = False
            break
    if no_minus:
        return [forms_of_operation[0], types_of_operation[1]]

    if nums[0][0] == "-" and nums[1][0] == "-":
        return [forms_of_operation[1], types_of_operation[1]]
    elif nums[0][0] != "-" and nums[1][0] == "-":
        return [forms_of_operation[2], types_of_operation[0]]
    else:
        return [forms_of_operation[3], types_of_operation[0]]


form_of_operation, type_of_operation = get_operation_type(nums)

# Swap numbers if necessary
if forms_of_operation[1] == form_of_operation:
    temp = nums[0]
    nums[0] = nums[1]
    nums[1] = temp


# Getting rid of minuses
for i in range(len(nums)):
    if nums[i][0] == "-":
        nums[i] = nums[i][1:]


# Make the numbers have same powers


def common_power(nums):
    getcontext().prec = 100000

    num_parts = []
    power_parts = []

    for i in range(len(nums)):
        if "e" not in nums[i]:
            num_parts.append(nums[i])
            power_parts.append(0)
        else:
            if nums[i].split("e")[1] == "":
                print("ERROR")
                return
            num_parts.append(Decimal(nums[i].split("e")[0]))
            power_parts.append(int(nums[i].split("e")[1]))

    max_power = max(power_parts[0], power_parts[1])

    for i in range(len(num_parts)):
        if power_parts[i] != 0:
            num_parts[i] *= Decimal("10") ** (power_parts[i] - max_power)

    return num_parts, power_parts, max_power


num_parts, power_parts, max_power = common_power(nums)


# We take decimal numbers and put them to a string with 0


def e_to_string(num):
    num = str(num)

    num = num.replace("E", "e")

    if "e" not in str(num):
        return num

    string = "0."
    [num, power] = num.split("e")
    string += "0" * int((math.fabs(int(power)) - 1))
    for i in range(len(num)):
        if num[i] == ".":
            continue

        string += num[i]

    return string


for i in range(len(num_parts)):
    num_parts[i] = e_to_string(num_parts[i])


# Take the strings and convert them to an array


def numstr_to_arr(numstr):
    arr = []
    for i in range(len(numstr)):
        if numstr[i] == ".":
            continue

        arr.append(int(numstr[i]))
    return arr


num_arrays = []

for i in range(len(num_parts)):
    num_arrays.append(numstr_to_arr(num_parts[i]))

max_len = max(len(num_arrays[0]), len(num_arrays[1]))

for i in range(len(num_arrays)):
    num_arrays[i].extend([0] * (max_len - len(num_arrays[i])))

# Now we compare the numbers


def compare_binary_numbers(num_arrays):
    for i in range(len(num_arrays[0])):
        bit1 = int(num_arrays[0][i])
        bit2 = int(num_arrays[1][i])

        if bit1 > bit2:
            return 0
        elif bit1 < bit2:
            return 1

    return "Equal"


bigger_num_index = compare_binary_numbers(num_arrays)


def addition(num_arrays):
    result_arr = []
    carry = 0

    for i in range(max_len - 1, -1, -1):
        bit1 = int(num_arrays[0][i])
        bit2 = int(num_arrays[1][i])

        temp_sum = bit1 + bit2 + carry
        result_bit = temp_sum % 2
        carry = temp_sum // 2

        result_arr.insert(0, str(result_bit))

    if carry:
        result_arr.insert(0, str(carry))

    return result_arr


def subtraction(num_arrays):
    result_arr = []

    for i in range(max_len - 1, -1, -1):
        res = (num_arrays[0][i] - num_arrays[1][i]) % 2

        result_arr.insert(0, res)

    return result_arr


# Now we need to figure out which operation to use and get result
def calculate(num_arrays):
    global max_power

    if type_of_operation == types_of_operation[0]:
        result_arr = addition(num_arrays)
        if len(result_arr) > max_len:
            max_power = int(max_power) - 1
    else:
        result_arr = subtraction(num_arrays)

    return result_arr


result_arr = calculate(num_arrays)

# Delete zeros at the end

for i in range(len(result_arr) - 1, 0, -1):
    if result_arr[i] == 0:
        result_arr.pop()
    else:
        break


# Deleting zeros at the start


while True:
    i = 0
    if result_arr[i] == 0:
        result_arr.pop(i)
        max_power += 1
        if i != len(result_arr):
            i += 1
        else:
            break
    else:
        break

if len(result_arr) != 1:
    result_arr.insert(1, ".")

# Create the result string

result_string = ""


for i in range(len(result_arr)):
    result_string += str(result_arr[i])

if max_power != 0:
    result_string += f"e{max_power}"


# Adding the minus sign

if form_of_operation == forms_of_operation[3]:
    result_string = "-" + result_string
    print(result_string)
elif type_of_operation == types_of_operation[1] and bigger_num_index == 1:
    result_string = "-" + result_string
    print(result_string)
elif bigger_num_index == "Equal":
    print(0)
else:
    print(result_string)
