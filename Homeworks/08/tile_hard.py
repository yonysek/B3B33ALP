import sys
import math
from copy import deepcopy
from PIL import Image, ImageDraw
from itertools import product
import time


def load_stones(filename):
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
        self.board = {}

        for p in range(-self.size, self.size):
            for q in range(-self.size, self.size):
                if self.in_board(p, q):
                    if p not in self.board:
                        self.board[p] = {}
                    self.board[p][q] = 0

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

    def in_board(self, p, q):
        return (
            (q >= 0)
            and (q < self.size)
            and (p >= -(q // 2))
            and (p < (self.size - q // 2))
        )

    def rotate_right(self, p, q):
        pp = -q
        qq = p + q
        return pp, qq

    def rotate_left(self, p, q):
        pp = p + q
        qq = -p
        return pp, qq

    def save_image(self, filename):
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
                    [cx - 3, cy - 3],
                    "{} {}".format(p, q),
                    fill="black",
                    anchor="mm",
                )
        img.save(filename)


# loading input file
size = int(sys.argv[1])
board = Board(size)
stones = load_stones(sys.argv[2])

board.save_image("progress.png")

game_board = board.board
final_board = None

stones = {i: stone for i, stone in enumerate(stones)}

stones_copy = deepcopy(stones)

first_key = list(game_board.keys())[0]
first_value = list(game_board[first_key].keys())[0]

# {0: [[0, 2], [1, 1], [-1, 2], [2, 0], [1, 0], [0, 0], [0, 1]], 1: [[1, 2], [2, 1]]}
# {0: (0, 2), 1: (1, 2)}


def place_stones():
    global final_board
    placed_stones = {}
    # tried_positions = {}
    p, q = first_key, first_value
    tried_rotations = {}

    i = 0

    while not board_is_full():
        if i == len(stones):
            return False

        if (p, q, i) not in tried_rotations:
            tried_rotations[(p, q, i)] = []

        if (
            can_place_stone(stones[i], p, q)
            and stones[i] not in tried_rotations[(p, q, i)]
        ):
            place_stone(stones[i], i, p, q)
            tried_rotations[(p, q, i)].append(stones[i])
            placed_stones[i] = (p, q)
            i += 1
            save_progress()
            p, q = first_key, first_value
        else:
            can_rotate = True

            tried_rotations[(p, q, i)].append(stones[i])

            for _ in range(6):
                rotated_stone = rotate_stone(stones[i])
                if rotated_stone not in tried_rotations[(p, q, i)]:
                    stones[i] = rotated_stone
                    can_rotate = True
                    break
                else:
                    can_rotate = False

            # print(stones[i])

            if not can_rotate:
                p, q = next_cell(p, q)

                if p is None:
                    if i == 0:
                        return False

                    for p in game_board.keys():
                        for q in game_board[p].keys():
                            if (p, q, i) in tried_rotations:
                                del tried_rotations[(p, q, i)]

                    i -= 1
                    p, q = placed_stones[i]

                    placed_stones = remove_stone(i, placed_stones)

    final_board = deepcopy(game_board)
    return True


def remove_stone(i, placed_stones):
    p, q = placed_stones[i]
    pivot = stones[i][0]

    for cell in stones[i]:
        game_board[p + cell[0] - pivot[0]][q + cell[1] - pivot[1]] = 0
    del placed_stones[i]
    save_progress()
    return placed_stones


def save_progress():
    # board.save_image("progress.png")
    # time.sleep(1)
    pass


def board_is_full():
    for i in game_board.keys():
        for j in game_board[i].keys():
            if game_board[i][j] == 0:
                return False
    return True


def next_cell(p, q):
    if p not in game_board.keys():
        return None, None
    col = game_board[p]
    if q + 1 in col.keys():
        return p, q + 1
    else:
        return p + 1, 0


def rotate_stone(stone):
    rotated_stone = []
    for cell in stone:
        rotated_stone.append([cell[0], cell[1]])
    rotated_stone = [
        list(board.rotate_right(cell[0], cell[1])) for cell in rotated_stone
    ]
    return rotated_stone


def can_place_stone(stone, row, col):
    pivot = stone[0]
    for cell in stone:
        # print(pivot, cell, col, row)
        if not board.in_board(row + cell[0] - pivot[0], col + cell[1] - pivot[1]):
            return False
        if game_board[row + cell[0] - pivot[0]][col + cell[1] - pivot[1]] != 0:
            return False
    return True


def place_stone(stone, i, row, col):
    if can_place_stone(stone, row, col):
        pivot = stone[0]
        for cell in stone:
            board.board[row + cell[0] - pivot[0]][col + cell[1] - pivot[1]] = i + 1


solution = place_stones()

board.save_image("final.png")


# creating output file
f = open(sys.argv[3], "w")
if solution:
    for p in final_board:
        for q in final_board[p]:
            f.write("{} {} {}\n".format(p, q, final_board[p][q]))
else:
    f.write("NOSOLUTION")
f.close()
