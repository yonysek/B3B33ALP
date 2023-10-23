array = [0, 1, 2, 3, 4, 5]

array.pop(2)

array = array[:2] + [2.1, 2.2] + array[2:]

print(array)
