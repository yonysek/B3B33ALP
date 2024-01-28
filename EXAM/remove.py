import sys
import string

file_path = sys.argv[1]

with open(file_path, "rt") as f:
    # Read the contents of the file
    contents = f.read()

alphabet = list(string.ascii_lowercase)
alphabet.extend(string.ascii_uppercase)


arr = contents.strip().split("\n")

arr = [word for word in arr if word != ""]

string = sys.argv[2]

stringArr = [s for s in string]

new = []
for s in stringArr:
    if s.lower() in stringArr:
        new.append(s.upper())
    if s.upper() in stringArr:
        new.append()

stringArr.extend(new)


def deletedLetters(word):
    count = 0
    newWord = ""
    for s in word:
        if s in stringArr:
            count += 1
            continue
        newWord += s

    remains = 0
    for s in newWord:
        if s in alphabet:
            remains += 1

    ratio = 0
    if count == 0:
        ratio = 1e69
    else:
        ratio = remains / count

    return count, remains, ratio, newWord


maxDel = -1
delIndex = [0]

maxRem = -1
remIndex = [0]

maxRat = -1
ratIndex = [0]

words = []

for i in range(len(arr)):
    de, rem, rat, word = deletedLetters(arr[i])

    words.append(word)

    if de > maxDel:
        maxDel = de
        delIndex = [i]
    elif de == maxDel:
        delIndex.append(i)

    if rem > maxRem:
        maxRem = rem
        remIndex = [i]
    elif rem == maxRem:
        remIndex.append(i)

    if rat > maxRat:
        maxRat = rat
        ratIndex = [i]
    elif rat == maxRat:
        ratIndex.append(i)


for i in delIndex:
    print(words[i])
for i in remIndex:
    print(words[i])
for i in ratIndex:
    print(words[i])
