import sys


def error():
    print("ERROR")
    sys.exit()


# input = input()
input = "eightythree"

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
    if type == "int":
        temp_error = False
        for i in range(len(input)):
            if temp_error:
                error()
            for j in range(9):
                if str(j) != input[i]:
                    temp_error = True
                else:
                    temp_error = False
                    break


error_check(input, type)


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
        string = string.split("hundred")[1]
    else:
        res_str += "0"

    for i in range(9):
        if string == num_strings[i]:
            res_str += f"0{nums[i]}"
            return res_str

    for i in range(10, 27):
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

    if rest != "":
        final_str = handle_str_hundreds(rest)
    if ths != "":
        final_str = handle_str_hundreds(ths) + final_str

    arr = list(final_str)
    while arr[0] == "0":
        arr.pop(0)

    actually_final_str = ""

    for i in range(len(arr)):
        actually_final_str += arr[i]

    return actually_final_str


print(handle_str_hundreds("two"))
print(str_to_int("twothousand"))
