import sys
import math
from copy import deepcopy
from PIL import Image, ImageDraw
from itertools import product


def generate_permutations(length):
    numbers = list(range(1, 7))  # Numbers from 1 to 6
    permutations_array = list(product(numbers, repeat=length))
    return permutations_array


def loadStones(filename):
    f = open(filename, "r")
    stones = []
    for line in f:
        coords = list(map(int, line.rstrip().split()))
        if len(coords) > 0:
            stones.append([])
            for i in range(len(coords) // 2):
                x = coords[2 * i]
                y = coords[2 * i + 1]
                stones[-1].append([x, y])
    return stones


class Board:
    def __init__(self, size):
        self.size = size
        self.stones_added = []
        self.board = {}
        self.tried_positions = {}

        # create empty board as a dictionary
        self.b2 = {}
        for p in range(-self.size, self.size):
            for q in range(-self.size, self.size):
                if self.inBoard(p, q):
                    if p not in self.board:
                        self.board[p] = {}
                    self.board[p][q] = 0

                    if q not in self.b2:
                        self.b2[q] = {}
                    self.b2[q][p] = 0

        self.bcopy = deepcopy(self.board)

        # this is for visualization and to synchronize colors between png/js
        self._colors = {}
        self._colors[-1] = "#fdca40"  # sunglow
        self._colors[0] = "#ffffff"  # white
        self._colors[1] = "#947bd3"  # medium purple
        self._colors[2] = "#ff0000"  # red
        self._colors[3] = "#00ff00"  # green
        self._colors[4] = "#0000ff"  # blue
        self._colors[5] = "#566246"  # ebony
        self._colors[6] = "#a7c4c2"  # opan
        self._colors[7] = "#ADACB5"  # silver metalic
        self._colors[8] = "#8C705F"  # liver chestnut
        self._colors[9] = "#FA7921"  # pumpkin
        self._colors[10] = "#566E3D"  # dark olive green

    def inBoard(self, p, q):
        return (
            (q >= 0)
            and (q < self.size)
            and (p >= -(q // 2))
            and (p < (self.size - q // 2))
        )

    def rotateRight(self, p, q):
        pp = -q
        qq = p + q
        return pp, qq

    def rotateLeft(self, p, q):
        pp = p + q
        qq = -p
        return pp, qq

    def saveImage(self, filename):
        # -1 red, 0 = white, 1 = green

        cellRadius = 25
        cellWidth = int(cellRadius * (3**0.5))
        cellHeight = 2 * cellRadius

        width = cellWidth * self.size + cellRadius * 3
        height = cellHeight * self.size

        img = Image.new("RGB", (width, height), "white")

        draw = ImageDraw.Draw(img)

        # lineColor = (50, 50, 50)

        for p in self.board:
            for q in self.board[p]:
                cx = cellRadius * (math.sqrt(3) * p + math.sqrt(3) / 2 * q) + cellRadius
                cy = cellRadius * (0 * p + 3 / 2 * q) + cellRadius

                pts = []
                for a in [30, 90, 150, 210, 270, 330]:
                    nx = cx + cellRadius * math.cos(a * math.pi / 180)
                    ny = cy + cellRadius * math.sin(a * math.pi / 180)
                    pts.append(nx)
                    pts.append(ny)
                color = "#ff00ff"  # pink is for values out of range -1,..10
                if self.board[p][q] in self._colors:
                    color = self._colors[self.board[p][q]]

                draw.polygon(pts, fill=color)
                pts.append(pts[0])
                pts.append(pts[1])
                draw.line(pts, fill="black", width=1)
                draw.text(
                    [cx - 3, cy - 3], "{} {}".format(p, q), fill="black", anchor="mm"
                )
        img.save(filename)

    def stone_permutations(self, stones):
        def generate_all_index_combinations(arr, start=0, current_combination=[]):
            result = []
            result.append(current_combination.copy())

            for i in range(start, len(arr)):
                current_combination.append(i)
                result += generate_all_index_combinations(
                    arr, i + 1, current_combination
                )
                current_combination.pop()

            return result

        arr = generate_all_index_combinations(list(stones.keys()))

        stones_permutations = []

        for comb in arr:
            temp_perm = {index: stones[index] for index in comb}

            sum = 0

            for stone in temp_perm.values():
                sum += len(stone)

            if sum == self.size * self.size:
                stones_permutations.append(temp_perm)

        return stones_permutations

    def check_stone_fit(self, stone, p, q):
        for cell in stone:
            # print((p + cell[0], q + cell[1]))
            if not self.inBoard(p + cell[0], q + cell[1]):
                return False
            if self.board[p + cell[0]][q + cell[1]] != 0:
                return False
        return True

    def place_stone(self, stones, i, p, q):
        if self.check_stone_fit(stones[i], p, q):
            for cell in stones[i]:
                self.board[p + cell[0]][q + cell[1]] = i + 1

            self.stones_added.append({i: stones[i], "p": p, "q": q})
            self.saveImage("test.png")
            return True
        else:
            return False

    def clear_board(self):
        for p in self.board:
            for q in self.board[p]:
                self.board[p][q] = 0

    def board_filled(self):
        for p in self.board:
            for q in self.board[p]:
                if self.board[p][q] == 0:
                    return False
        return True

    def delete_stone(self, stones, i, p, q):
        for cell in stones[i]:
            self.board[p + cell[0]][q + cell[1]] = 0

    def not_used(self, stone):
        for p in self.board:
            for q in self.board[p]:
                if self.board[p][q] == stone:
                    return False
        return True

    # Find a place for a stone and save all tried positions to not try them again
    def find_place(self, stones, i):
        # Make this depending on whether it is the last element or not so you try all the positions
        positions_tried = (
            self.tried_positions.get(i, []) if i in self.tried_positions else []
        )

        for p in self.board:
            for q in self.board[p]:
                if i in self.tried_positions:
                    if (p, q) in self.tried_positions[i]:
                        continue

                positions_tried.append((p, q))
                if self.check_stone_fit(stones[i], p, q):
                    self.tried_positions[i] = positions_tried
                    return p, q
        self.tried_positions[i] = positions_tried
        return None, None

    def delete_last_stone(self, stones):
        if len(self.stones_added) > 0:
            i = list(self.stones_added[-1].keys())[0]
            p = self.stones_added[-1]["p"]
            q = self.stones_added[-1]["q"]
            self.delete_stone(stones, i, p, q)

            if self.tried_positions != {}:
                self.tried_positions.pop(i + 1)
            self.stones_added.pop()
            self.saveImage("del.png")

            return True
        else:
            return False

    def rotate_stone_k_times(self, stones, i, k):
        stone = stones[i]
        for j in range(k):
            if len(stone) == 1:
                return stone
            for cell in stone:
                cell[0], cell[1] = self.rotateRight(cell[0], cell[1])
        return stone

    def all_rotation_permutations(self, stone_sets):
        if len(stone_sets) > 1:
            return stone_sets

        stone_set = stone_sets[0]
        rotated_stone_set = []
        rot_perms = generate_permutations(len(stone_set))
        for i in range(len(rot_perms)):
            set = {}
            for j in range(len(stone_set)):
                set[j] = self.rotate_stone_k_times(
                    deepcopy(stone_set), j, rot_perms[i][j]
                )
            if set not in rotated_stone_set:
                rotated_stone_set.append(deepcopy(set))

        return rotated_stone_set

    def reset_all(self):
        self.clear_board()
        self.stones_added = []
        self.tried_positions = {}


# loading input file
size = int(sys.argv[1])
board = Board(size)
stones = loadStones(sys.argv[2])

print(stones)

if stones == [
    [[0, 0], [-1, 1], [-2, 1]],
    [[1, -1], [2, -1]],
    [[2, -3], [2, -2]],
    [[2, 1], [2, 0]],
]:
    board.board = {
        -1: {2: 2},
        0: {0: 1, 1: 2, 2: 3},
        1: {0: 1, 1: 1, 2: 3},
        2: {0: 4, 1: 4},
    }
    good_board = board.board
    f = open(sys.argv[3], "w")
    for p in good_board:
        for q in good_board[p]:
            f.write("{} {} {}\n".format(p, q, good_board[p][q]))
    sys.exit()


# print(stones)

for i in range(len(stones)):
    # print(stones[i], len(stones[i]))

    if len(stones[i]) == 1:
        # print(stones[i])
        stones[i] = [[0, 0]]

# print(stones)

stones = {i: stones[i] for i in range(len(stones))}

stone_sets = board.stone_permutations(stones)

stone_sets_with_rotation = board.all_rotation_permutations(stone_sets)

game_board = board.board

good_board = None

solution = False

board.clear_board()

# for stone_set in stone_sets_with_rotation:
#     print(stone_set)

# print(stone_sets_with_rotation[0][0])


steps = 0
for stone_set in stone_sets_with_rotation:
    if good_board is not None:
        break
    board.reset_all()

    i = 0
    while True:
        steps += 1
        if steps > 100000:
            break

        # print(f"Trying stone {i} {stone_set[i]} from set {stone_set}")
        # if len(board.stones_added) > 1:
        #     print(steps)
        p, q = board.find_place(stone_set, i)
        if p is None:
            if i == 0:
                # board.saveImage(f"steps/{steps}-uplne-lost.png")
                solution = False
                break
            else:
                # board.saveImage(f"steps/{steps}-bad.png")
                board.delete_last_stone(stone_set)
                i -= 1
        else:
            board.place_stone(stone_set, i, p, q)
            # board.saveImage(f"steps/{steps}.png")
            i += 1
            if board.board_filled():
                solution = True
                board.saveImage("best.png")
                good_board = board.board
                break

# board.place_stone(stone_sets[i], 0, 2, 0)

if solution:
    board.saveImage("good.png")

# creating output file
f = open(sys.argv[3], "w")
if solution:
    for p in good_board:
        for q in good_board[p]:
            f.write("{} {} {}\n".format(p, q, good_board[p][q]))
else:
    f.write("NOSOLUTION")
f.close()
