import math

import copy


import sys

xd = 69


if xd == 69:
    f = open(sys.argv[1], "rt")
else:
    f = open("B3B33ALP/Homeworks/05/dama.txt", "rt")

# Read the contents of the file
contents = f.read()

# Split the contents into rows
rows = contents.strip().split("\n")

# Split each row into columns
board = [list(map(int, row.split())) for row in rows]


# Create heuristic based on distance from desired position

size = len(board)


def printBoard(board):
    length = len(board) + 2
    newBoard = [["k" for i in range(length)] for j in range(length)]
    newBoard[0][1] = "j"
    newBoard[1][0] = "i"
    for i in range(2, len(newBoard)):
        newBoard[0][i] = i - 2
    for i in range(2, len(newBoard)):
        newBoard[i][0] = i - 2

    for i in range(len(board)):
        for j in range(len(board[i])):
            newBoard[i + 2][j + 2] = board[i][j]

    max_widths = [max(map(lambda x: len(str(x)), col)) for col in zip(*newBoard)]

    for row in newBoard:
        for value, width in zip(row, max_widths):
            if "k" in str(value):
                print(" " * width, end=" ")
                continue
            print(f"{value:{width}}", end=" ")
        print()
    print()


def desired(board):
    i4, j4 = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 4:
                i4, j4 = i, j
    return i4, j4


def bishop(board):
    i2, j2 = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 2:
                i2, j2 = i, j
    return i2, j2


def distance(board):
    i4, j4 = desired(board)

    distanceBoard = copy.deepcopy(board)

    for i in range(len(board)):
        for j in range(len(board[i])):
            distanceBoard[i][j] = abs(i - i4) + abs(j - j4)

    return distanceBoard


distanceBoard = distance(board)


def inBoard(i, j):
    if i < 0 or j < 0 or i > size - 1 or j > size - 1:
        return False
    return True


def markDiagonal(board, distanceBoard):
    i4, j4 = desired(board)

    direction = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    for i in range(4):
        dir = direction[i]

        step = 1
        while True:
            newI = i4 + dir[0] * step
            newJ = j4 + dir[1] * step
            if not inBoard(newI, newJ) or board[newI][newJ] == 1:
                break

            distanceBoard[newI][newJ] = 1

            step += 1

    return distanceBoard


def possibleMoves(board):
    i2, j2 = bishop(board)

    direction = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    moves = []

    for i in range(4):
        dir = direction[i]

        step = 1
        while True:
            newI = i2 + dir[0] * step
            newJ = j2 + dir[1] * step
            if not inBoard(newI, newJ) or board[newI][newJ] == 1:
                break

            moves.append((newI, newJ))

            step += 1

    return moves


def sortMovesToQueue(moves):
    moveDict = {}

    for move in moves:
        i, j = move
        value = distanceBoard[i][j]

        if value not in moveDict:
            moveDict[value] = [move]
            continue

        moveDict[value].append(move)

    sortedKeys = list(moveDict.keys())

    sortedKeys.sort()

    sortedMoves = []

    for key in sortedKeys:
        for move in moveDict[key]:
            sortedMoves.append(move)

    return sortedMoves


def createBoardWithPos(board, i, j):
    i2, j2 = bishop(board)

    newBoard = copy.deepcopy(board)

    newBoard[i2][j2] = 0

    newBoard[i][j] = 2

    return newBoard


def end(pos):
    for i in pos:
        if len(pos[i]) != 0:
            return False

    return True


def coords_to_chessboard(coords):
    return chr(coords[1] + 97) + str(size - coords[0])


instant = possibleMoves(board)

for i, j in instant:
    if distanceBoard[i][j] == 0:
        print(coords_to_chessboard((i, j)))


def posMoveBoard(board):
    posBoard = copy.deepcopy(board)

    for i in range(len(board)):
        for j in range(len(board[i])):
            newBoard = createBoardWithPos(board, i, j)

            posMoves = possibleMoves(newBoard)

            posBoard[i][j] = posMoves

    return posBoard


posBoard = posMoveBoard(board)

tried = []

# I give up
