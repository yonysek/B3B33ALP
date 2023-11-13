seq = input()
# seq = "5 10 12 13 15 18"
# seq = "440 1196 1478 405 874 652 217 1488 136 1137 407 796 1208 411 1602 1498 453 1085 1016 596 308 931 975 1226 1562"
# seq = "442 81 268 419 10 214 92 57 53 355 236 23 282 411"

seq = seq.split()
seq = [int(x) for x in seq]

sums = input()
# sums = "30"
# sums = "1718 2499"
# sums = "412 2474"
#  268 81 53 10;442 419 411 355 282 236 214 92 23

sums = sums.split()
sums = [int(x) for x in sums]


def set_cur(cur, indexes, seq):
    cur = 0
    for i in indexes:
        cur += seq[i]

    return cur


def find_subsequences_with_sum(seq, target_sum):
    cur = 0
    indexes = []

    res_indexes = []

    i = 0
    while True:
        indexes.append(i) if i < len(seq) else None
        cur = set_cur(cur, indexes, seq)

        if cur == target_sum:
            res_indexes.append(indexes.copy())
            i = indexes.pop() + 1
            continue

        if indexes == []:
            break

        if cur > target_sum:
            i = indexes.pop() + 1
            cur = set_cur(cur, indexes, seq)
        else:
            i += 1

        if i >= len(seq) and cur != target_sum:
            i = indexes.pop()
            cur = set_cur(cur, indexes, seq)

            i += 1

    res_sequences = []
    for i in range(len(res_indexes)):
        res_seq = []
        for j in range(len(res_indexes[i])):
            res_seq.append(seq[res_indexes[i][j]])
        res_sequences.append(res_seq)

    return res_sequences


sums1 = find_subsequences_with_sum(seq, sums[0])


if sums1 == []:
    print("NEEXISTUJE")
    exit()

sums2 = []

for i in range(len(sums1)):
    copy_seq = seq.copy()
    copy_seq = [x for x in copy_seq if x not in sums1[i]]
    if find_subsequences_with_sum(copy_seq, sums[1]) != []:
        sums1 = sums1[i]
        sums2 = find_subsequences_with_sum(copy_seq, sums[1])[0]
        break


if sums2 == []:
    print("NEEXISTUJE")
    exit()


both_sums = [sums1, sums2]

for i in range(len(both_sums)):
    both_sums[i].sort(reverse=True)
    for j in range(len(both_sums[i])):
        print(both_sums[i][j], end=" ")
    print("")
