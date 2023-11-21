# import copy
import math

# import random
from PIL import Image, ImageDraw


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
        self.board = {}

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
        """return True if (p,q) is valid coordinate"""
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
            if not self.inBoard(p + cell[0], q + cell[1]):
                return False
            if self.board[p + cell[0]][q + cell[1]] != 0:
                return False
        return True

    def place_stone(self, stones, i, p, q):
        if self.check_stone_fit(stones[i], p, q):
            for cell in stones[i]:
                self.board[p + cell[0]][q + cell[1]] = i + 1
            self.saveImage(f"{i}_tile.png")
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


# count number of cells then try fitting all lists of available stones to the board :) fit iteratively from top left
