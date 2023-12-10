import copy
import math
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
    def __init__(self, size=0):
        self.size = size
        self.board = {}

        # create empty board as a dictionary
        self.b2 = {}
        for p in range(-self.size, self.size):
            for q in range(-self.size, self.size):
                if self.inBoard(p, q):
                    if not p in self.board:
                        self.board[p] = {}
                    self.board[p][q] = 0

                    if not q in self.b2:
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
        """draw actual board to png"""

        cellRadius = 60
        cellWidth = int(cellRadius * (3**0.5))
        cellHeight = 2 * cellRadius

        width = cellWidth * self.size + cellRadius * 3
        height = cellHeight * self.size

        img = Image.new("RGB", (width, height), "white")

        draw = ImageDraw.Draw(img)

        lineColor = (50, 50, 50)

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
                    [cx - 3, cy - 3], "{} {}".format(p, q), fill="black", anchor="m"
                )
        img.save(filename)

    def loadBoard(self, filename):
        board = {}
        fread = open(filename, "rt")
        size = -1
        for line in fread:
            p, q, value = list(map(int, line.strip().split()))
            size = max(size, q)
            if p not in board:
                board[p] = {}
            board[p][q] = value
        fread.close()
        self.board = board
        self.size = size + 1


b = Board(0)
b.loadBoard("B3B33ALP/Homeworks/09/board.txt")
# b.loadBoard(sys.argv[1])
b_copy = {}

for p in b.board:
    b_copy[p] = {}
    for q in b.board[p]:
        b_copy[p][q] = b.board[p][q]
        if b.board[p][q] == 2:
            spider_p = p
            spider_q = q

direction = ((0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0))


def surroundings(b, p, q):
    o = [0] * 6
    for i in range(6):
        if b.inBoard(p + direction[i][0], q + direction[i][1]):
            o[i] = b.board[p + direction[i][0]][q + direction[i][1]]
        else:
            o[i] = -1
    return o


o_spider = surroundings(b, spider_p, spider_q)


def spider_move(p, q, o):
    possible_moves = []
    for i in range(6):
        if o[i] == 0 and (
            (o[(i - 1) % 6] == 0 and o[(i + 1) % 6] == 1)
            or (o[(i - 1) % 6] == 1 and o[(i + 1) % 6] == 0)
        ):
            # print(direction[i])
            possible_moves.append([p + direction[i][0], q + direction[i][1]])
    return possible_moves


# print(spider_move(spider_p, spider_q, o_spider))


components = 0
for i in range(6):
    if o_spider[i] == 1 and o_spider[(i + 1) % 6] != 1:
        components += 1


pos = [[spider_p, spider_q]]
dont_go_back = pos[:]
b.board[spider_p][spider_q] = 0

for i in range(3):
    pos2 = []
    # print(i, pos)
    for p, q in pos:
        possible = spider_move(p, q, surroundings(b, p, q))
        for x in possible:
            if x not in dont_go_back:
                pos2.append(x)
                dont_go_back.append(x)
            else:
                # print("back")
                pass

    pos = pos2[:]

print(pos2)
