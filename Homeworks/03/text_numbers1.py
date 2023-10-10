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


error = False
final_str = ""

# input = input()
input = "eightythree"

input_type = ""

for i in range(len(nums)):
    if str(nums[i]) in input:
        input_type = "int"
        break
    elif str(num_strings[i]) in input:
        input_type = "str"
        break
    else:
        error = True

valid_num = True
if input_type == "int":
    for i in range(len(input)):
        if input[i] not in nums_as_strings and input[i] != "0":
            valid_num = False
            break

# Basic case

if input_type == "str":
    for i in range(len(num_strings)):
        if num_strings[i] == input:
            final_str = nums[i]

    def split_number(input):
        ths = ""
        rest = input
        if "thousand" in input:
            ths, rest = input.split("thousand")
        return ths, rest

    ths, rest = split_number(input)

    def handle_hundreds(num):
        global error

        res_str = ""
        if "hundred" in num:
            if num.split("hundred")[0] == "":
                res_str += "1"
            else:
                error = True
                return "69"

            for i in range(0, 9):
                if num_strings[i] == num.split("hundred")[0]:
                    res_str += str(nums[i])
                    error = False
                else:
                    error = True
                    return "69"

            if num.split("hundred")[1] == "":
                res_str += "00"
                return res_str

            num = num.split("hundred")[1]
        else:
            res_str += "0"

        for i in range(9):
            if num == num_strings[i]:
                res_str += f"0{nums[i]}"
                return res_str

        for i in range(10, 27):
            if num == num_strings[i]:
                res_str += str(nums[i])
                return res_str

            if num_strings[i] in num:
                res_str += str(nums[i])[0]
                num = num.split(num_strings[i])[1]

                for i in range(9):
                    if num == num_strings[i]:
                        res_str += str(nums[i])
                        return res_str

        error = True
        return "69"

    if error != True:
        final_str = handle_hundreds(rest)
        if ths != "":
            final_str = handle_hundreds(ths) + final_str

        arr = list(final_str)
        while arr[0] == "0":
            arr.pop(0)

        actually_final_str = ""

        for i in range(len(arr)):
            actually_final_str += arr[i]

    if error:
        print("ERROR")
    else:
        print(actually_final_str)

elif input_type == "int" and valid_num == True:
    ths = ""
    rest = ""

    if len(input) > 3:
        rest = input[-3:]
        ths = input[:-3]
    else:
        rest = input

    def handle_hundreds(num):
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
            for i in range(27):
                if num == str(nums[i]):
                    res_str += num_strings[i]
                    return res_str

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

    final_str = handle_hundreds(rest)
    print(final_str)
    if ths != "":
        ths = handle_hundreds(ths)
        final_str = ths + "thousand" + final_str

    print(final_str)


else:
    print("ERROR")
