import math
from decimal import Decimal, getcontext

# # # input = input()


# # def decimal_to_arr(str):
# #   if "e" not in str:
# #     num_part = str
# #     power_part = 0
# #   else:
# #     num_part = str.split('e')[0]
# #     power_part = str.split('e')[1]
# #   arr = [0] * int(math.fabs(int(power_part)))
# #   for i in range(len(num_part)):
# #     if num_part[i] == ".": 
# #       continue
# #     arr.append(int(num_part[i]))
# #   return arr
  

# # # print(decimal_to_arr(1e-10))
# # # print(decimal_to_arr(1.1))


# # def subtraction(num_1, num_2):
# #   nums = [str(num_1), str(num_2)]
# #   highest_power = 0
# #   lowest_power = 0
# #   for i in range(len(nums)):
# #     if "e" in str(nums[i]):
# #       if i == 0 or int(nums[i].split("e")[1]) > highest_power:
# #         highest_power = int(nums[i].split("e")[1])
# #       if i == 0 or int(nums[i].split("e")[1]) < lowest_power:
# #         lowest_power = nums[i].split("e")[1]
# #   print(highest_power, lowest_power)



# # print(decimal_to_arr("1.101011e110"))
# # # subtraction("1.123123e-110", "1.123e13")



# num1 = "1.1001010e-13"
# num2 = "1.0111e23"

# nums = [num1, num2]




# def max_power(nums):
#   for i in range(len(nums)):


#     if "e" not in nums[i]:
#       power_part = 0
#       if i == 0:
#         highest_power = power_part
#         lowest_power = power_part
#     else:
#       power_part = int(nums[i].split("e")[1])
#       if i == 0:
#         highest_power = power_part
#         lowest_power = power_part

#     highest_power = max(highest_power, power_part)
#     lowest_power = min(lowest_power, power_part)
#   return [highest_power, lowest_power]

# def num_parts(nums):
#   num_parts = []
#   for i in range(len(nums)):

#     if "e" not in nums[i]:
#       num_parts.append(float(nums[i]))
#     else:
#       num_part = nums[i].split("e")[0]
#       if num_part[-1] == "0":

#         for j in range(len(num_part) - 1, 0, -1):

#           if num_part[j] == "1":
#             num_part = num_part[:j-1]
#             break

#       num_parts.append(float(num_part))



#   return num_parts

# [highest_power, lowest_power] = max_power(nums)
# [num1, num2] = num_parts(nums)


# arr_length = 2

# if highest_power > 0 and lowest_power > 0:
#   if len(num1) > highest_power or len(num2) > highest_power:
#     arr_length = 69
#   arr_length = highest_power

# arr_length = max_power(nums)[0] + max_power(nums)[1] + num_parts(nums)[1]


num1 = "1010010011" 
num2 = "0000101111"

nums = [num1, num2]

# num1 = input()
# num2 = input()

# for i in range(len(nums)):
#   if len(nums[i]) == "1":
#     break
#   else:
#     if nums[i][0] != 1 or nums




# def common_power(num1, num2):
#   num_part1, power_part1 = num1.split("e")
#   num_part2, power_part2 = num2.split("e")

#   num_part1 = float(num_part1)
#   num_part2 = float(num_part2)
#   power_part1 = int(power_part1)
#   power_part2 = int(power_part2)

#   max_power = max(power_part1, power_part2)

#   num_part1 *= 10**(power_part1 - max_power)
#   num_part2 *= 10**(power_part2 - max_power)

#   print(num_part1, num_part2)





# dostanes nejakou mrdku s tim eckem tak to prevedes na string jakoze chytre proste to co pajton neumi
# 1.3e-4 = "0.00013" a uz k tomu nemusis dat to e neco pac to bude stejny, odectes a ezLLLLLL


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
  


def numstr_to_arr(numstr):
  arr = []
  for i in range(len(numstr)):
    if numstr[i] == ".":
      continue

    arr.append(int(numstr[i]))
  return arr



def common_power(num1, num2):
    
    getcontext().prec = 1000


   


    if "e" not in num1:
      num_part1, power_part1 = num1, 0
    else:
      if num1.split("e")[1] == "":
        print("ERORR")
        return
      num_part1, power_part1 = num1.split("e")
    if "e" not in num2:
      num_part2, power_part2 = num2, 0
    else:
      if num2.split("e")[1] == "":
        print("ERORR")
        return
      num_part2, power_part2 = num2.split("e")


    

    num_part1 = Decimal(num_part1)
    num_part2 = Decimal(num_part2)
    power_part1 = int(power_part1)
    power_part2 = int(power_part2)

    max_power = max(power_part1, power_part2)

    num_part1 *= Decimal('10')**(power_part1 - max_power)
    num_part2 *= Decimal('10')**(power_part2 - max_power)


    num_string1 = e_to_string(num_part1)
    num_string2 = e_to_string(num_part2)

    arr1 = numstr_to_arr(num_string1)
    arr2 = numstr_to_arr(num_string2)



    max_len = max(len(arr1), len(arr2))



    arr1.extend([0] * (max_len - len(arr1)))
    arr2.extend([0] * (max_len - len(arr2)))


    result_arr = []


    for i in range(max_len):
      if arr1[i] == 0 and arr2[i] == 0:
        result_arr.append(0)
      elif arr1[i] == 1 and arr2[i] == 0:
        result_arr.append(1)
      elif arr1[i] == 0 and arr2[i] == 1:
        result_arr.append(0)
      elif arr1[i] == 1 and arr2[i] == 1:
        result_arr.append((arr1[i] - arr2[i] + 2) % 2)


    result_arr.insert(1, ".")


    for i in range(len(result_arr) - 1, 0, -1):
      if result_arr[i] == 0:
        result_arr.pop()
      else:
        break


    res_to_str = ""
    for i in range(len(result_arr)):
      res_to_str += str(result_arr[i])

    res_to_float = Decimal(res_to_str)



    if "E" in str(res_to_float):
      power = int(str(res_to_float).split("E")[1]) + max_power
      print(f"{str(res_to_float).split('E')[0]}e{power}")
      return

    print(f"{str(res_to_float)}e{max_power}")



common_power(num1,num2)





