input1 = input()
input2 = input()

# input2 = "0.7 3.2 1.65 0.6 -4.3 3.7 -3.6 4.65 -2.85 3.1 -4.45 -4.65 -0.25 0.95"
# input1 = "0.15 3.45 2.0 1.3 3.5 3.5 -1.55 -2.25 -3.95 1.95 -0.4 -1.1 -0.4 4.6"

row1 = list(map(float, input1.split()))
row2 = list(map(float, input2.split()))

if row1 == [] or row2 == []:
    print("ERROR")
    exit()

if len(row1) != len(row2):
    print("ERROR")
    exit()

# row1 = [0.0, 1.0, -1.0, 0.5]
# row2 = [1.0, 0.0, -1.0, -1.5]


def func_val(x, y):
    equals = 1 / 2 * (x**2) * (1 - y) ** 2 + (x - 2) ** 3 - 2 * y + x
    return equals


max_val = None
max_index = 0

for i in range(len(row1)):
    if max_val is None:
        max_val = func_val(row1[0], row2[0])

    res = func_val(row1[i], row2[i])
    if max_val < res:
        max_val = res
        max_index = i


under_zero = 0
for i in range(len(row1)):
    if func_val(row1[i], row2[i]) < 0:
        under_zero += 1


indexes = [0]


def new_func(x, y):
    return func_val(x, y) * (x + 2) * (y - 2)


for i in range(len(row1)):
    res = new_func(row1[i], row2[i])
    if res in indexes:
        indexes.append(i)

    for j in range(len(indexes)):
        if res < new_func(row1[indexes[j]], row2[indexes[j]]):
            indexes = []
            indexes.append(i)


print(max_index, under_zero, min(indexes))
