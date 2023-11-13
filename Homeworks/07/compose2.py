seq = input()

seq = seq.split()
seq = [int(x) for x in seq]

sums = input()
sums = sums.split()
sums = [int(x) for x in sums]


def find_subsequences_with_sum(sequence, target_sum, index=None):
    if index is None:
        index = len(sequence) - 1

    if index == 0:
        return [[sequence[0]]] if sequence[0] == target_sum else [[]]

    # Exclude the current element
    exclude = find_subsequences_with_sum(sequence, target_sum, index=index - 1)

    # Include the current element
    include = find_subsequences_with_sum(
        sequence, target_sum - sequence[index], index=index - 1
    )

    # Include the current element in each subsequence
    include_with_current = [sub + [sequence[index]] for sub in include]

    # Combine all possibilities
    result = exclude + include_with_current

    # Add only subsequences that sum up to the target sum
    result = [subseq for subseq in result if sum(subseq) == target_sum]

    return result


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
