# Find blacks (around 1's and around other numbers when they could share it)
# Use dict for each numbers island (somehow) and check above properties at all times
# Find unreachable cells (distance)


import sys

s = 0
if s == 0:
    with open(
        "/Users/yonysek/Library/CloudStorage/GoogleDrive-vybirjon@fel.cvut.cz/My Drive/Winter 2023:24/B3B33ALP/Homeworks/10/board.txt",
        "r",
    ) as file:
        board = file.read()
else:
    board = sys.argv[1]

# DOWN RIGHT UP LEFT
directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

diagonals = ((-1, 1), (-1, -1), (1, -1), (1, 1))


board = board.split("\n")

boardList = []
for i in board:
    temp = []
    i = i.split(" ")
    for j in range(len(i)):
        temp.append(int(i[j]))
    boardList.append(temp)


islands = {}

for i in range(len(boardList)):
    for j in range(len(boardList)):
        el = boardList[i][j]
        appendix = 0
        keysIs = list(islands.keys())
        for k in range(len(keysIs), 0, -1):
            k = k - 1
            key = int(str(keysIs[k]).split(".")[0])
            keyAppendix = int(str(keysIs[k]).split(".")[1])
            if el == key:
                appendix = keyAppendix + 1
                break
        if el not in [-1, 0]:
            el = float(f"{str(el)}.{appendix}")
            islands[el] = (i, j)


def changeBoard():
    for k in islands:
        i, j = islands[k]
        boardList[i][j] = k


changeBoard()


def getElNum(board, i, j):
    if board[i][j] > 0:
        return int(str(board[i][j]).split(".")[0])
    else:
        return board[i][j]


def checkBoardFor(board, el):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == el:
                return True
    return False


def inBoard(board, i, j):
    if i < 0 or j < 0 or i > len(board) - 1 or j > len(board) - 1:
        return False
    else:
        return True


def printBoard(board):
    for i in board:
        print(i)


def lonelyRiver(board, i, j):
    if not checkBoardFor(board, 0):
        return False

    for k in range(len(directions)):
        lonely = True
        iC = i + directions[k][0]
        jC = j + directions[k][1]
        if inBoard(board, iC, jC):
            if board[iC][jC] in [0, -1]:
                lonely = False

    return lonely


def findPool(board):
    poolDirection = ((1, 0), (0, 1), (1, 1))
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                numOfBlacks = 1
                notBlack = []
                for k in range(len(poolDirection)):
                    iC = i + poolDirection[k][0]
                    jC = j + poolDirection[k][1]
                    if inBoard(board, iC, jC):
                        if board[iC][jC] == 0:
                            numOfBlacks += 1
                        else:
                            notBlack = [iC, jC]
                if numOfBlacks == 3:
                    return notBlack
    return None


def markAroundOnes():
    for i in range(len(boardList)):
        for j in range(len(boardList[i])):
            if boardList[i][j] == 1:
                for k in range(len(directions)):
                    iC = i + directions[k][0]
                    jC = j + directions[k][1]
                    if inBoard(boardList, iC, jC):
                        boardList[iC][jC] = 0


def distance(board, i, j, toI, toJ):
    distance = abs(toI - i) + abs(toJ - j)
    return distance


def reachableTiles(board, i, j):
    reachableTiles = [[i, j]]
    d = board[i][j]
    for k in range(d - 1, 0, -1):
        for iC in range(len(board)):
            for jC in range(len(board)):
                if distance(board, i, j, iC, jC) == k:
                    reachableTiles.append([iC, jC])
    return reachableTiles


def markUnreachableTiles(board):
    availableTiles = []
    orgIslands = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] > 0:
                orgIslands.append([i, j])
    for k in orgIslands:
        i, j = k
        availableTiles.extend(reachableTiles(board, i, j))

    for i in range(len(board)):
        for j in range(len(board)):
            if [i, j] not in availableTiles:
                board[i][j] = 0


def diagonalMark(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] > 0:
                for k in diagonals:
                    iC = i + k[0]
                    jC = j + k[1]
                    if not inBoard(board, iC, jC):
                        continue
                    if board[iC][jC] > 1:
                        board[i + k[0]][j] = 0
                        board[i][j + k[1]] = 0


def markInterspace(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] > 0:
                for k in range(len(directions)):
                    iC = i + 2 * directions[k][0]
                    jC = j + 2 * directions[k][1]
                    if not inBoard(board, iC, jC):
                        continue
                    if board[iC][jC] > 0:
                        board[i + directions[k][0]][j + directions[k][1]] = 0


printBoard(boardList)
markInterspace(boardList)
printBoard(boardList)


# def isValid(board):
#     placeToCheck = []
#     for i in range(len(board)):
#         for j in range(len(board[i])):
#             if board[i][j] != -1:
#                 placeToCheck.append([i, j])
#     print(placeToCheck, len(placeToCheck))


# isValid(boardList)
