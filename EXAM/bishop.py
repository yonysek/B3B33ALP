import sys

# Open the board file
f = open(sys.argv[1], "rt")

# Read the contents of the file
contents = f.read()

# Split the contents into rows
rows = contents.strip().split("\n")

# Split each row into columns
board = [list(map(int, row.split())) for row in rows]

directions = [(1, 1), (1, -1), (-1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]
size = len(board)

start = None
end = None

for i in range(len(board)):
    for j in range(len(board[i])):
        if board[i][j] == 2:
            start = (i, j)
        if board[i][j] == 4:
            end = (i, j)


reached = [[0 for i in range(len(board))] for j in range(len(board))]
reached[start[0]][start[1]] = 1


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

def coords_to_chessboard(coords):
    return chr(coords[1] + 97) + str(size - coords[0])


def solve():
    step = [[start[0], start[1], ""]]

    step_num = 1

    while len(step) > 0:
        new_steps = []
        for position in step:
            pi = position[0]
            pj = position[1]
            for direction in directions:
                newI = pi
                newJ = pj
                while True:
                    newI = newI + direction[0]
                    newJ = newJ + direction[1]

                    if direction == (0,1):
                        print(newI, newJ)

                    if newI < 0 or newI >= size or newJ < 0 or newJ >= size:
                        break
                    if board[newI][newJ] not in [0,4] or reached[newI][newJ] not in [0, step_num]:
                        break


                    reached[newI][newJ] = step_num

                    printBoard(reached)

                    new_steps.append([newI, newJ, position[2] + " " + coords_to_chessboard((newI, newJ))])

                    if (newI, newJ) == end:
                        print(position[2] + " " + coords_to_chessboard((newI, newJ)))
                        quit()




        print(new_steps)
        step = new_steps
        step_num += 1


solve()

print("NO SOLUTION")