# lst = "-1 -2 -3 6 -1 -2 -3 5"
# lst = "3 3 3 3 3 3 3 3 3"
# lst = "76 20 99 92 52 -7 51 26 97 61 16 21 0 38 18 57 -17 11 55 57 43 95 25 79 36 14 -7 37 -10 86 80 74 59 1 -6 -20 91 84 65 69 66 11 76 2 40 -7 10 62 28 5 22 84 47 -19 33 96 99 92 52 -7 51 26 97 61 16 21 0 38 54 72"

lst = input()

lst = list(map(int, lst.split()))

largest_array = [None, None, 0, -999999999]  # index1, index2, len
for i, num in enumerate(lst):
    for j, actual_num in enumerate([None] * (i + 1) + lst[i + 1 :]):
        if actual_num == None:
            continue
        if num == actual_num:
            lst1 = lst[i:j]
            lst2 = lst[j:]
            sum = 0
            length = 0

            for _ in range(min(len(lst1), len(lst2))):
                if lst1[length] != lst2[length]:
                    break
                sum += lst1[length]
                length += 1
                if largest_array[3] < sum:
                    largest_array = [i, j, length, sum]


print(largest_array[2], largest_array[3])
