import sys

dict = open(sys.argv[1], "rt")
dict = dict.read()

dict = [x.strip() for x in dict.split("\n") if x.strip() != ""]

# print(dict)

postfix = sys.argv[2]

validWords = []

for i in dict:
    wordSize = len(i)
    postfixSize = len(postfix)
    partToCheck = i[wordSize - postfixSize :]
    if partToCheck == postfix:
        validWords.append(i)


length = len(validWords)
if length == 0:
    print(0)
    print(None)
    quit()

print(length)

shortestLen = len(validWords[0])
shortest = validWords[0]

for i in validWords:
    if len(i) < shortestLen:
        shortestLen = len(i)
        shortest = i

print(shortest)
