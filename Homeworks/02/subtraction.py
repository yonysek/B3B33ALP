import math
from decimal import Decimal, getcontext
import sys


# Inputs

num1 = input()
num2 = input()


# num1 = "1.011"
# num2 = "1.11011011001001001e110"

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


# Converting binary powers to decimal powers


def powers_from_bin(power):
    negative = False
    if "-" in power:
        negative = True
        power = power[1:]
    power = int(f"0b{power}", 2)
    if negative:
        power = int(f"-{power}")

    return power


# Moving decimal according to the scientific notation
def move_decimal(float_num, power):
    if power == 0:
        return str(float_num)
    float_str = str(float_num)

    integer_part, _, fractional_part = float_str.partition(".")

    if power < 0:
        adjusted_str = "0." + "0" * abs(abs(power) - 1) + integer_part + fractional_part
    else:
        adjusted_str = integer_part + fractional_part + "0" * power

    return adjusted_str


def contain_only_one_minus_sign(input_str):
    minus = False
    for char in input_str:
        if minus == False and char == "-":
            minus = True
        elif minus == True and char == "-":
            print("ERROR")
            sys.exit()


def contain_only_one_e(input_str):
    minus = False
    for char in input_str:
        if minus == False and char == "e":
            minus = True
        elif minus == True and char == "e":
            print("ERROR")
            sys.exit()


def contains_only_valid_characters(input_str):
    valid_characters = set(["-", "0", "1", "e", "."])

    for char in input_str:
        if char not in valid_characters:
            return False

    return True


for i in range(len(nums)):
    if contains_only_valid_characters(nums[i]) == False:
        print("ERROR")
        sys.exit()
    contain_only_one_minus_sign(nums[i])
    contain_only_one_e(nums[i])
    if nums[i][0] == "0":
        print("ERROR")
        sys.exit()
    if num1 == "" or num2 == "":
        print("ERROR")
        sys.exit()
    if "e" in nums[i] and "." not in nums[i].split("e")[0]:
        print("ERROR")
        sys.exit()

# Function to check whether the string contains only valid characters


def contains_only_valid_power_characters(input_str):
    valid_characters = set(["-", "0", "1"])

    for char in input_str:
        if char not in valid_characters:
            return False

    return True


def common_power(nums):
    getcontext().prec = 100000

    num_parts = []
    power_parts = []

    for i in range(len(nums)):
        if "e" not in nums[i]:
            num_parts.append(nums[i])
            power_parts.append(0)
        else:
            if (
                nums[i].split("e")[1] == ""
                or contains_only_valid_power_characters(nums[i].split("e")[1]) == False
            ):
                print("ERROR")
                sys.exit()

            num_parts.append(Decimal(nums[i].split("e")[0]))
            # power_parts.append(int(nums[i].split("e")[1]))
            power_parts.append(powers_from_bin(nums[i].split("e")[1]))

    max_power = max(power_parts[0], power_parts[1])

    for i in range(len(num_parts)):
        num_parts[i] = move_decimal(num_parts[i], power_parts[i] - max_power)

    return num_parts, power_parts, max_power


# TODO Ask whether we just need the first print ERROR and then it can just crash
num_parts, power_parts, max_power = common_power(nums)


# Getting rid of decimal dot and padding with zeros

for i in range(len(num_parts)):
    num_parts[i] = num_parts[i].replace(".", "")

max_len = max(len(num_parts[0]), len(num_parts[1]))

for i in range(len(num_parts)):
    num_parts[i] += (max_len - len(num_parts[i])) * "0"


# Convert the strings to arrays because we need to have numbers inside

num_arrays = []

for i in range(len(num_parts)):
    arr = []
    for j in range(len(num_parts[i])):
        arr.append(int(num_parts[i][j]))
    num_arrays.append(arr)


# print(num_parts[0])
# print(num_parts[1])
# print(num_arrays[0])
# print(num_arrays[1])
# print(len(num_parts[0]))


# We now need to compare the numbers


def compare_binary_numbers(num_arrays):
    for i in range(len(num_arrays[0])):
        bit1 = int(num_arrays[0][i])
        bit2 = int(num_arrays[1][i])

        # If we are dealing with subtraction and the first number is smaller than the second number, we need to add minus sign to the expression at the end
        if bit1 > bit2:
            return 0
        elif bit1 < bit2:
            return 1

    print(0)
    sys.exit()


bigger_num_index = compare_binary_numbers(num_arrays)


def addition(num_arrays):
    result_arr = []
    carry = 0

    max_len = max(len(num_arrays[0]), len(num_arrays[1]))

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
    max_len = max(len(num_arrays[0]), len(num_arrays[1]))
    carry = 0
    for i in range(max_len - 1, -1, -1):
        diff = num_arrays[0][i] - num_arrays[1][i] - carry
        if diff < 0:
            diff += 2
            carry = 1
        else:
            carry = 0
        result_arr.insert(0, diff % 2)
    return result_arr


def calculate(num_arrays):
    global max_power

    if type_of_operation == types_of_operation[0]:
        result_arr = addition(num_arrays)
        if len(result_arr) > max_len:
            max_power = int(max_power) + 1
    else:
        if bigger_num_index == 1:
            num_arrays[0], num_arrays[1] = num_arrays[1], num_arrays[0]
        result_arr = subtraction(num_arrays)

    return result_arr


result_arr = calculate(num_arrays)

# print(result_arr)
# print(len(result_arr))


# TODO Here it should be like somehow working but I wouldn't bet my life on it

# Delete zeros at the end

for i in range(len(result_arr) - 1, 0, -1):
    if int(result_arr[i]) == 0:
        result_arr.pop()
    else:
        break

# Deleting zeros at the start

while True:
    i = 0
    if result_arr[i] == 0:
        result_arr.pop(i)
        max_power -= 1
        if i != len(result_arr):
            i += 1
        else:
            break
    else:
        break

# Adding the decimal point

if len(result_arr) != 1:
    result_arr.insert(1, ".")


# Create the result string

result_string = ""

for i in range(len(result_arr)):
    result_string += str(result_arr[i])

# Adding the exponent in binary and handling the sign

if max_power != 0:
    max_power = bin(max_power)
    if "-" in max_power:
        max_power = max_power[0] + max_power[3:]
    else:
        max_power = max_power[2:]
    result_string += f"e{max_power}"


# Adding the minus sign

if form_of_operation == forms_of_operation[3]:
    result_string = "-" + result_string
    print(result_string)
elif type_of_operation == types_of_operation[1] and bigger_num_index == 1:
    result_string = "-" + result_string
    print(result_string)
else:
    print(result_string)
