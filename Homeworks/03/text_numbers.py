import sys


def error():
    print("ERROR")
    sys.exit()


input = input()
# input = "69"

num_strings = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
    "hundred",
    "thousand",
]

nums = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
    1000,
]

nums_as_strings = [str(num) for num in nums]

types = ["str", "int"]

type = "error"


for i in range(len(num_strings)):
    if num_strings[i] in input:
        type = types[0]
        break
    elif nums_as_strings[i] in input:
        type = types[1]
        break

if type == "error":
    error()


def error_check(input, type):
    if type == "str":
        for i in range(9):
            if str(i) in input:
                error()
        if "thousand" in input:
            without_thousand = input.replace("thousand", "", 1)
            if "thousand" in without_thousand:
                error()

        for i in range(10):
            if str(i) in input:
                error()

    if type == "int":
        temp_error = False
        for i in range(len(input)):
            for j in range(10):
                if str(j) != input[i]:
                    temp_error = True
                else:
                    temp_error = False
                    break
            if temp_error:
                error()


error_check(input, type)

# Funtion to check if the hundreds in the string is correct


def check_str_hundreds(string):
    org_str = string
    if "hundred" in string:
        string = string.replace("hundred", "", 1)
        if "hundred" in string:
            error()

        string = org_str.split("hundred")[0]
        for i in range(9, 27):
            if num_strings[i] in string:
                error()

    temp_str = ""
    for i in range(9, 27):
        if num_strings[i] in string:
            # string = string.replace(num_strings[i], "", 1)

            temp_str = string.split(num_strings[i])[0]

            if temp_str != "":
                temp_str = string.split(num_strings[i])[0]

    for i in range(0, 27):
        if num_strings[i] in temp_str:
            error()

    # Checking if the string is even valid
    temp_err = True
    for i in range(len(num_strings)):
        if num_strings[i] in org_str:
            temp_err = False
            break

    if temp_err:
        error()

    return org_str


# Funtion to handle hundreds in string


def handle_str_hundreds(string):
    res_str = ""
    if "hundred" in string:
        if string.split("hundred")[0] == "":
            res_str += "1"

        for i in range(0, 9):
            if num_strings[i] == string.split("hundred")[0]:
                res_str += str(nums[i])
        if string.split("hundred")[1] == "":
            res_str += "00"
            return res_str
        string = string.split("hundred")[1]
    else:
        res_str += "0"

    for i in range(9):
        if string == num_strings[i]:
            res_str += f"0{nums[i]}"
            return res_str

    for i in range(9, 27):
        if string == num_strings[i]:
            res_str += str(nums[i])
            return res_str

        if num_strings[i] in string:
            res_str += str(nums[i])[0]
            string = string.split(num_strings[i])[1]

            for i in range(9):
                if string == num_strings[i]:
                    res_str += str(nums[i])
                    return res_str


# Funtion to convert string to int
def str_to_int(input):
    final_str = ""
    # Just one string representation
    for i in range(len(num_strings)):
        if num_strings[i] == input:
            final_str = nums[i]

    # Splitting the string with thousands
    ths = ""
    rest = input
    if "thousand" in input:
        ths, rest = input.split("thousand")

    if ths == "" and rest == "":
        final_str = 1000
        return final_str

    if rest:
        checked_str = check_str_hundreds(rest)
        # print("checked str: ", checked_str)
        final_str = handle_str_hundreds(checked_str)
        # print("converted str: ", final_str)
    else:
        final_str = "000"

    if ths:
        checked_str = check_str_hundreds(ths)
        final_str = handle_str_hundreds(checked_str) + final_str

    arr = list(final_str)
    while arr[0] == "0":
        arr.pop(0)

    actually_final_str = ""

    for i in range(len(arr)):
        actually_final_str += arr[i]

    return actually_final_str


def illegal_duos(num):
    for i in range(0, 19):
        for j in range(len(num_strings) - 2):
            illegal_duo = f"{num_strings[i]}{num_strings[j]}"
            if illegal_duo in input:
                error()
    for i in range(19, len(num_strings) - 2):
        for j in range(10, 19):
            illegal_duo = f"{num_strings[i]}{num_strings[j]}"
            if illegal_duo in input:
                error()


illegal_duos(input)


def handle_int_hundreds(num):
    res_str = ""
    if len(num) == 3:
        for i in range(9):
            if num[0] == str(nums[i]):
                res_str += f"{num_strings[i]}hundred"
                break
        if num[1:] == "00":
            return res_str

        num = num[1:]
    if len(num) == 2:
        # Check if the rest is just some valid number
        for i in range(27):
            if num == str(nums[i]):
                res_str += num_strings[i]
                return res_str

        # Check if the rest is some of the tens
        for i in range(2, 10):
            if num[0] == str(i):
                res_str += num_strings[17 + i]
                for j in range(9):
                    if num[1] == str(nums[j]):
                        res_str += num_strings[j]
                        return res_str
                res_str += "0"
                return res_str
        for i in range(9):
            if num[1] == str(nums[i]):
                res_str += num_strings[i]
                return res_str

    if len(num) == 1:
        for j in range(9):
            if num[0] == str(nums[j]):
                res_str += num_strings[j]
                return res_str
        res_str += "0"
        return res_str


# Funtion to convert int to string
def int_to_str(input):
    ths = ""
    rest = ""

    if len(input) > 3:
        rest = input[-3:]
        ths = input[:-3]
    else:
        rest = input

    final_str = handle_int_hundreds(rest)
    if ths:
        ths = handle_int_hundreds(ths)
        final_str = ths + "thousand" + final_str

    return final_str


if type == "str":
    print(str_to_int(input))
else:
    print(int_to_str(input))


# print(str_to_int("sixtynine"))

# print(str_to_int(input))
