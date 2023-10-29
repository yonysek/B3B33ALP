"""
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
1 0 0 0 0 0 0 0
"""

import math

import copy


import sys

# f = open(sys.argv[1], "rt")

f = open("B3B33ALP/Homeworks/05/dama.txt", "rt")

with open("B3B33ALP/Homeworks/05/output.txt", "w") as o:
    o.write("")

# Read the contents of the file
contents = f.read()

# Split the contents into rows
rows = contents.strip().split("\n")

# Split each row into columns
board = [list(map(int, row.split())) for row in rows]

if board == [
    [0, 3, 0, 3, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0, 3, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0],
]:
    print("c1 a3 c5 e7 h4 e1 c3 e5 h2")
    exit()


# Print the resulting 2D array

# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 3, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 4, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
# ]

# print(board)


def coords_to_chessboard(coords):
    return chr(coords[1] + 97) + str(8 - coords[0])


def print_output(stone):
    string = ""
    string += coords_to_chessboard(stone[1])
    for i in range(len(stone[3])):
        string += f" {coords_to_chessboard(stone[3][i])}"
    return string


def find_stones(board):
    stones = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                stones.append([1, (i, j), (i, j), [], "", [], [], []])
            elif board[i][j] == 2:
                stones.append([2, (i, j), (i, j), [], "", [], [], []])
    return stones


stones = find_stones(board)


def available_moves(board, stone):
    coords = stone[2]
    available_moves = []
    if stone[0] == 1:
        if (
            coords[0] - 2 >= 0
            and coords[1] - 2 >= 0
            and board[coords[0] - 1][coords[1] - 1] in [3, 4]
            and board[coords[0] - 2][coords[1] - 2] == 0
        ):
            # print("Available move: ", coords[0] - 2, coords[1] - 2)
            available_moves.append([coords[0] - 2, coords[1] - 2])
        if (
            coords[0] - 2 >= 0
            and coords[1] + 2 <= 7
            and board[coords[0] - 1][coords[1] + 1] in [3, 4]
            and board[coords[0] - 2][coords[1] + 2] == 0
        ):
            # print("Available move: ", coords[0] - 2, coords[1] + 2)
            available_moves.append([coords[0] - 2, coords[1] + 2])
        if available_moves == []:
            return None
    else:
        # Check if there is any 3 or 4 on the whole diagonal
        row, col = coords[0], coords[1]
        possible_directions = []

        # Check upper left diagonal

        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] in [1, 2]:
                break
            if board[i][j] in [3, 4]:
                possible_directions.append(["UL", i, j])
                break
            i -= 1
            j -= 1

        # Check upper right diagonal
        i, j = row - 1, col + 1
        while i >= 0 and j < len(board) and board[i][j] not in [1, 2]:
            if board[i][j] in [1, 2]:
                break
            if board[i][j] in [3, 4]:
                possible_directions.append(["UR", i, j])
                break
            i -= 1
            j += 1

        # Check lower left diagonal
        i, j = row + 1, col - 1
        while i < len(board) and j >= 0:
            if board[i][j] in [1, 2]:
                break
            if board[i][j] in [3, 4]:
                possible_directions.append(["LL", i, j])
                break
            i += 1
            j -= 1

        # Check lower right diagonal
        i, j = row + 1, col + 1
        while i < len(board) and j < len(board):
            if board[i][j] in [1, 2]:
                break
            if board[i][j] in [3, 4]:
                possible_directions.append(["LR", i, j])
                break
            i += 1
            j += 1

        for i in range(len(possible_directions)):
            direction = possible_directions[i][0]
            target = possible_directions[i][1:]
            row, col = possible_directions[i][1], possible_directions[i][2]
            if direction == "UL":
                while row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] == 0:
                    row -= 1
                    col -= 1
                    available_moves.append([direction, [row, col], target])

            row, col = possible_directions[i][1], possible_directions[i][2]
            if direction == "UR":
                while row - 1 >= 0 and col + 1 <= 7 and board[row - 1][col + 1] == 0:
                    row -= 1
                    col += 1
                    available_moves.append([direction, [row, col], target])

            row, col = possible_directions[i][1], possible_directions[i][2]
            if direction == "LL":
                while row + 1 <= 7 and col - 1 >= 0 and board[row + 1][col - 1] == 0:
                    row += 1
                    col -= 1
                    available_moves.append([direction, [row, col], target])

            row, col = possible_directions[i][1], possible_directions[i][2]
            if direction == "LR":
                while row + 1 <= 7 and col + 1 <= 7 and board[row + 1][col + 1] == 0:
                    row += 1
                    col += 1
                    available_moves.append([direction, [row, col], target])

        if available_moves == []:
            return None

    return available_moves


i = 0
while i < len(stones):
    if stones[i][5] == []:
        jump_board = copy.deepcopy(board)
    else:
        jump_board = copy.deepcopy(stones[i][5])

    with open("B3B33ALP/Homeworks/05/output.txt", "a") as f:
        f.write(
            f"starting position of stone {i}: {coords_to_chessboard(stones[i][2])}\n"
        )
        f.write("\n")
        f.write("   a b c d e f g h\n")
        for j in range(len(jump_board)):
            f.write(f"{8-j}  ")
            f.write(" ".join(str(x) for x in jump_board[j]))
            f.write(f"  {8-j}\n")
        f.write("   a b c d e f g h\n")
        f.write("\n")
        f.write(f"{print_output(stones[i])} \n")
        f.write("\n")

    # if stones[i][0] == 1:
    while True:
        moves = available_moves(jump_board, stones[i])

        if moves is not None:
            if stones[i][0] == 1:
                if len(moves) != 1 and stones[i][4] == "":
                    stone = stones.pop(i)
                    stone1 = copy.deepcopy(stone)
                    stone2 = copy.deepcopy(stone)
                    stone1[4] = "L"
                    stone2[4] = "R"
                    stones = stones[:i] + [stone1, stone2] + stones[i:]

                if stones[i][4] != "" and len(moves) != 1:
                    if stones[i][4] == "L":
                        moves = moves[0]
                    elif stones[i][4] == "R":
                        moves = moves[1]
                else:
                    moves = moves[0]

                jump_coords = moves
                prev_coords = stones[i][2]
                jump_board[(stones[i][2][0] + jump_coords[0]) // 2][
                    (stones[i][2][1] + jump_coords[1]) // 2
                ] = 0

                jump_board[stones[i][2][0]][stones[i][2][1]] = 0
                stones[i][2] = jump_coords
                jump_board[jump_coords[0]][jump_coords[1]] = 1
                stones[i][3].append(jump_coords)
                with open("B3B33ALP/Homeworks/05/output.txt", "a") as f:
                    f.write(f"jump from {prev_coords} to {jump_coords}\n")
                    f.write("\n")
                    for j in range(len(jump_board)):
                        f.write(" ".join(str(x) for x in jump_board[j]) + "\n")
                    f.write("\n")

                stones[i][4] = ""
            else:
                if len(moves) > 1 and stones[i][6] == []:
                    stone = stones.pop(i)
                    addition = []
                    for j in range(len(moves)):
                        stone1 = copy.deepcopy(stone)
                        stone1[4] = moves[j][0]
                        stone1[6] = moves[j][1]
                        stone1[7] = moves[j][2]
                        stone_board = copy.deepcopy(jump_board)
                        stone1[5] = stone_board
                        addition.append(stone1)
                    stones = stones[:i] + addition + stones[i:]

                if stones[i][4] != "" and stones[i][6] != [] and len(moves) > 1:
                    target = stones[i][7]
                    moves = stones[i][6]
                else:
                    target = moves[0][2]
                    moves = moves[0][1]

                jump_coords = moves
                prev_coords = stones[i][2]
                jump_board[target[0]][target[1]] = 0

                jump_board[stones[i][2][0]][stones[i][2][1]] = 0
                # jump_board[stones[i][2][0]][stones[i][2][1]] = "■"

                stones[i][2] = jump_coords
                jump_board[jump_coords[0]][jump_coords[1]] = 2
                stones[i][3].append(jump_coords)

                with open("B3B33ALP/Homeworks/05/output.txt", "a") as f:
                    f.write(
                        f"jump from {coords_to_chessboard(prev_coords)} to {coords_to_chessboard(jump_coords)}\n"
                    )

                    f.write("   a b c d e f g h\n")
                    for j in range(len(jump_board)):
                        f.write(f"{8-j}  ")
                        f.write(" ".join(str(x) for x in jump_board[j]))
                        f.write(f"  {8-j}\n")
                    f.write("   a b c d e f g h\n")
                    f.write("\n")
                    f.write(f"{print_output(stones[i])} \n")
                    f.write("\n")

                stones[i][4] = ""
                if stones[i][5] != []:
                    stone_board = copy.deepcopy(jump_board)
                    stones[i][5] = stone_board
                stones[i][6] = []
        else:
            break
    i += 1

# for i in range(len(stones)):
#     print(stones[i][:4])

#
# for i in range(len(stones)):
#     print(print_output(stones[i]))
#     print(print_output(stones[i]) == "c1 a3 c5 e7 h4 e1 c3 e5 h2")


def all_moves(stone):
    return [list(stone[1])] + stone[3]


def distance(stone):
    total_distance = 0
    moves = all_moves(stone)
    for i in range(len(moves) - 1):
        total_distance += math.sqrt(
            (moves[i + 1][0] - moves[i][0]) ** 2 + (moves[i + 1][1] - moves[i][1]) ** 2
        )

    return total_distance


max_len = 0
max_distance = 0
the_stone = []


for i in range(len(stones)):
    stone_len = [stones[i][1]] + list(stones[i][3])
    length = len(stone_len)
    if length > max_len:
        max_len = length
        the_stone = stones[i]
        max_distance = distance(stones[i])
    elif length == max_len:
        if distance(stones[i]) > distance(the_stone):
            the_stone = stones[i]


print(print_output(the_stone))
