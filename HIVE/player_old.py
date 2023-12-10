import base as Base
import copy, random, time, math
from PIL import Image, ImageDraw
import random

# TODO If there is a move that is next to enemy queen it's a good move


class Player(Base.Board):
    def __init__(
        self, playerName, myIsUpper, size, myPieces, rivalPieces
    ):  # do not change this line
        Base.Board.__init__(
            self, myIsUpper, size, myPieces, rivalPieces
        )  # do not change this line
        self.playerName = playerName
        self.algorithmName = "honey"
        self.isUpper = myIsUpper

        self.allies = [i for i in self.myPieces]
        self.enemies = [i for i in self.rivalPieces]
        self.direction = ((0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0))
        self.myPiecesCopy = copy.deepcopy(myPieces)

    def getAllEmptyCells(self):
        result = []
        for p in self.board:
            for q in self.board[p]:
                if self.isEmpty(p, q, self.board):
                    result.append([p, q])
        return result

    def getAllNonemptyCells(self):
        result = []
        for p in self.board:
            for q in self.board[p]:
                if not self.isEmpty(p, q, self.board):
                    result.append([p, q])
        return result

    def getAllMyCells(self):
        result = []
        for p in self.board:
            for q in self.board[p]:
                if not self.isEmpty(p, q, self.board):
                    if self.board[p][q][-1].isupper() == self.isUpper():
                        result.append([p, q])
        return result

    def isAll(self, pos):
        for i in pos:
            if i not in self.getAllMyCells():
                return False
        return True

    def move(self):
        if self.start():
            return self.startingMove()

        emptyCells = self.border()

        if len(emptyCells) == 0:
            return []

        if self.myMove == 1:
            p, q = self.randomlyPlace()
            return [self.fixUpper("q"), None, None, p, q]

        if self.myMove == 2:
            p, q = self.randomlyPlace()
            return [self.fixUpper("a"), None, None, p, q]

        # for animal in self.myPieces:
        #     if (
        #         self.myPieces[animal] > 0
        #     ):  # is this animal still available? if so, let's place it
        #         p, q = self.randomlyPlace()
        #         return [animal, None, None, p, q]

        # randomCell = emptyCells[random.randint(0, len(emptyCells) - 1)]
        # randomP, randomQ = randomCell

        # allFigures = self.getAllNonemptyCells()
        # randomCell = allFigures[random.randint(0, len(allFigures) - 1)]
        # randomFigureP, randomFigureQ = randomCell

        # # Find a random move that doesn't break the hive
        # while True:
        #     if self.willBreakHive(randomFigureP, randomFigureQ, randomP, randomQ):
        #         randomCell = emptyCells[random.randint(0, len(emptyCells) - 1)]
        #         randomP, randomQ = randomCell

        #         allFigures = self.getAllNonemptyCells()
        #         randomCell = allFigures[random.randint(0, len(allFigures) - 1)]
        #         randomFigureP, randomFigureQ = randomCell
        #     else:
        #         break

        # animal = self.board[randomFigureP][randomFigureQ][-1]

        random = self.random()

        print("random", random)

        if random is None:
            quit()
            return []

        animal, p, q, newP, newQ = self.random()

        return [animal, p, q, newP, newQ]

    def fixUpper(self, animal):
        if self.isUpper:
            return animal.upper()
        else:
            return animal.lower()

    def start(self):
        sum = 0
        for p in self.board:
            for q in self.board[p]:
                if not self.isEmpty(p, q, self.board):
                    sum += 1

        if sum < 2:
            return True
        else:
            return False

    def startingMove(self):
        sum = 0
        for p in self.board:
            for q in self.board[p]:
                if not self.isEmpty(p, q, self.board):
                    sum += 1

        if sum == 0:
            return [self.fixUpper("g"), None, None, 3, 6]
        elif sum == 1:
            return [self.fixUpper("g"), None, None, 2, 7]

    def getRandomAnimal(self):
        availableAnimals = [i for i in self.myPieces if self.myPieces[i] > 0]
        if len(availableAnimals) == 0:
            return False
        animal = availableAnimals[random.randint(0, len(availableAnimals) - 1)]
        return animal

    def validPlacement(self, p, q):
        numOfAllies = 0

        if not self.isEmpty(p, q, self.board):
            return False

        positionsToCheck = [
            [p - 1, q],
            [p - 1, q + 1],
            [p, q - 1],
            [p, q],
            [p, q + 1],
            [p + 1, q - 1],
            [p + 1, q],
        ]

        for k in positionsToCheck:
            i = k[0]
            j = k[1]

            if i not in self.board:
                return False
            if j not in self.board[i]:
                return False

            if self.board[i][j] in self.enemies:
                return False

            if self.board[i][j] in self.allies:
                numOfAllies += 1

        if numOfAllies > 0:
            return True
        else:
            return False

    def getAllValidPlacements(self):
        result = []
        for p in self.board:
            for q in self.board[p]:
                if self.validPlacement(p, q):
                    result.append([p, q])
        return result

    def randomlyPlace(self):
        validPlacements = self.getAllValidPlacements()
        if len(validPlacements) == 0:
            return None, None
        randomPlacement = validPlacements[random.randint(0, len(validPlacements) - 1)]
        return randomPlacement

    def willBreakHive(self, p, q, newP, newQ):
        testBoard = copy.deepcopy(self.board)

        animal = testBoard[p][q][-1]
        testBoard[p][q] = testBoard[p][q][:-1]

        # if animal == "b":
        #     self.board = testBoard
        #     self.saveImage("b.png")
        #     quit()

        island = self.findIsland(testBoard)
        allCells = []

        for x in testBoard:
            for y in testBoard[x]:
                if testBoard[x][y] != "":
                    allCells.append([x, y])

        for i in allCells:
            if i not in island:
                return True

        if testBoard[newP][newQ] != "":
            return False

        testBoard[newP][newQ] += animal

        island = self.findIsland(testBoard)
        allCells = []

        for x in testBoard:
            for y in testBoard[x]:
                if testBoard[x][y] != "":
                    allCells.append([x, y])

        for i in allCells:
            if i not in island:
                return True

        return False

    # Used for willBreakHive. Finds a random cell and then looks through its surroundings.
    def findIsland(self, board):
        island = []

        isBroken = False

        for p in board:
            if isBroken:
                break
            for q in board[p]:
                if isBroken:
                    break
                if self.inBoard(p, q) and board[p][q] != "":
                    island.append([p, q])
                    isBroken = True

        i = 0
        while True:
            cell = island[i]
            neighbours = self.neighbours(board, cell[0], cell[1])
            for k in neighbours:
                if k not in island:
                    island.append(k)
            i += 1
            if i > len(island) - 1:
                break

        return island

    def checkSurroundings(self, board, p, q):
        surroundingsCoords = [
            [p - 1, q],
            [p - 1, q + 1],
            [p, q - 1],
            [p, q + 1],
            [p + 1, q - 1],
            [p + 1, q],
        ]

        surroundings = []

        for k in surroundingsCoords:
            i = k[0]
            j = k[1]

            if i not in board:
                continue
            if j not in board[i]:
                continue

            surroundings.append([i, j])

        return surroundings

    def binarySurroundings(self, board, p, q):
        o = [0] * 6
        for i in range(6):
            if (p + self.direction[i][0]) in board:
                if (q + self.direction[i][1]) in board[p + self.direction[i][0]]:
                    pos = board[p + self.direction[i][0]][q + self.direction[i][1]]
                    if pos in self.enemies or pos in self.allies:
                        o[i] = 1
                    else:
                        o[i] = 0
            else:
                o[i] = -1

        return o

    def neighbours(self, board, p, q):
        surroundings = self.checkSurroundings(board, p, q)
        neighbours = []
        for k in surroundings:
            pos = board[k[0]][k[1]]
            if pos in self.enemies or pos in self.allies:
                neighbours.append([k[0], k[1]])
        return neighbours

    def asqMove(self, p, q):
        o = self.binarySurroundings(self.board, p, q)

        possibleMoves = []
        for i in range(6):
            if o[i] == 0 and (
                (o[(i - 1) % 6] == 0 and o[(i + 1) % 6] == 1)
                or (o[(i - 1) % 6] == 1 and o[(i + 1) % 6] == 0)
            ):
                possibleMoves.append(
                    [p + self.direction[i][0], q + self.direction[i][1]]
                )
        return possibleMoves

    def newSurroudingsPleaseKillMe(self, board, p, q):
        o = [0] * 6
        for i in range(6):
            if (p + self.direction[i][0]) in board:
                if (q + self.direction[i][1]) in board[p + self.direction[i][0]]:
                    pos = [p + self.direction[i][0], q + self.direction[i][1]]
                    o[i] = pos

                else:
                    o[i] = -1

        return o

    def posPos(self, p, q, n):
        board = copy.deepcopy(self.board)
        o_p, o_q = p, q

        pos = [[p, q]]

        dontGoBack = pos[:]
        board[p][q] = 0

        for i in range(n):
            pos2 = []
            for p, q in pos:
                possible = self.asqMove(p, q)
                for x in possible:
                    if x not in dontGoBack:
                        pos2.append(x)
                        dontGoBack.append(x)
                    else:
                        pass

            pos = pos2[:]

        print("positions before check", pos2)

        posPos = []

        for i in pos2:
            if not self.inBoard(i[0], i[1]):
                continue
            if not self.willBreakHive(o_p, o_q, i[0], i[1]):
                posPos.append(i)

        print("positions after check", pos2)

        return posPos

    def checkMoves(self, p, q, moves):
        checkedMoves = []
        for i in moves:
            if not self.inBoard(i[0], i[1]):
                continue

            if not self.willBreakHive(p, q, i[0], i[1]):
                checkedMoves.append(i)
        return checkedMoves

    def getValidMoves(self, p, q):
        animal = self.board[p][q][-1]
        moves = []
        if animal.isupper() != self.isUpper():
            return moves

        animal = animal.lower()

        if animal == "a":
            moves = self.getValidMovesAnt(p, q)
        elif animal == "b":
            moves = self.getValidMovesBeetle(p, q)
        elif animal == "g":
            moves = self.getValidMovesGrasshopper(p, q)
        elif animal == "q":
            moves = self.getValidMovesQueen(p, q)
        elif animal == "s":
            moves = self.getValidMovesSpider(p, q)

        print("well it checked so it should be here", moves)

        return moves

    def getValidMovesSpider(self, p, q):
        return self.posPos(p, q, 3)

    def getValidMovesQueen(self, p, q):
        return self.posPos(p, q, 1)

    def getValidMovesAnt(self, p, q):
        moves = []
        n = 1
        while True:
            addition = self.posPos(p, q, n)

            if len(addition) == 0:
                break
            moves.extend(addition)
            n += 1

        return moves

    def getValidMovesBeetle(self, p, q):
        o = self.newSurroudingsPleaseKillMe(self.board, p, q)

        moves = []
        for i in o:
            if i == -1:
                continue
            else:
                moves.append(i)

        moves = self.checkMoves(p, q, moves)

        return moves

    def getValidMovesGrasshopper(self, p, q):
        moves = []
        for i in range(6):
            new_p, new_q = p, q
            if not self.inBoard(p + self.direction[i][0], q + self.direction[i][1]):
                continue
            if self.board[p + self.direction[i][0]][q + self.direction[i][1]] != "":
                while True:
                    if not self.inBoard(new_p, new_q):
                        break
                    new_p += self.direction[i][0]
                    new_q += self.direction[i][1]
                    if self.board[new_p][new_q] == "":
                        moves.append([new_p, new_q])
                        break

        moves = self.checkMoves(p, q, moves)

        return moves

    def getRandomMyPiece(self):
        while True:
            allFigures = self.getAllNonemptyCells()
            randomCell = allFigures[random.randint(0, len(allFigures) - 1)]
            randomFigureP, randomFigureQ = randomCell

            animal = self.board[randomFigureP][randomFigureQ][-1]

            if animal in self.myPiecesCopy:
                return randomFigureP, randomFigureQ
                break

    def random(self):
        type = None

        if self.getRandomAnimal():
            rand = random.randint(0, 1)
            if rand == 0:
                type = "place"
            else:
                type = "move"
        else:
            type = "move"

        if type == "place":
            animal = self.getRandomAnimal()
            p, q = self.randomlyPlace()
            return [animal, None, None, p, q]

        elif type == "move":
            i = 0
            allMyCells = self.getAllMyCells()
            while True:
                if i > len(allMyCells) - 1:
                    return None
                cell = allMyCells[i]
                print(cell)
                p, q = cell
                animal = self.board[p][q][-1]
                moves = self.getValidMoves(p, q)
                if len(moves) == 0 or moves is None:
                    i += 1
                    continue
                else:
                    break

            move = moves[random.randint(0, len(moves) - 1)]

            return [animal, p, q, move[0], move[1]]


def updatePlayers(move, activePlayer, passivePlayer):
    """write move made by activePlayer player
    this method assumes that all moves are correct, no checking is made
    """
    if len(move) == 0:
        return

    animal, p, q, newp, newq = move
    if p is None and q is None:
        # placing new animal
        activePlayer.myPieces[animal] -= 1
        passivePlayer.rivalPieces = activePlayer.myPieces.copy()
    else:
        # just moving animal
        # delete its old position
        activePlayer.board[p][q] = activePlayer.board[p][q][:-1]
        passivePlayer.board[p][q] = passivePlayer.board[p][q][:-1]

    activePlayer.board[newp][newq] += animal
    passivePlayer.board[newp][newq] += animal


if __name__ == "__main__":
    boardSize = 13
    smallFigures = {
        "q": 1,
        "a": 2,
        "b": 2,
        "s": 2,
        "g": 2,
    }  # key is animal, value is how many is available for placing
    bigFigures = {
        figure.upper(): smallFigures[figure] for figure in smallFigures
    }  # same, but with upper case

    P1 = Player("player1", False, 13, smallFigures, bigFigures)
    P2 = Player("player2", True, 13, bigFigures, smallFigures)

    filename = "begin.png"
    P1.saveImage(filename)

    moveIdx = 0
    while True:
        print(P1.board)
        move = P1.move()
        print(moveIdx, "P1 returned", move, P1.isUpper)
        updatePlayers(move, P1, P2)  # update P1 and P2 according to the move
        filename = "moves/move-{:03d}-player1.png".format(moveIdx)
        # filename = "progress.png"
        P1.saveImage(filename)
        # time.sleep(0.5)

        print(P2.board)
        move = P2.move()
        print(moveIdx, "P2 returned", move)
        updatePlayers(move, P2, P1)  # update P2 and P1 according to the move
        filename = "moves/move-{:03d}-player2.png".format(moveIdx)
        P1.saveImage(filename)
        # time.sleep(0.5)

        moveIdx += 1
        P1.myMove = moveIdx
        P2.myMove = moveIdx

        # print(P1.myPieces)
        # print(P2.myPieces)

        if moveIdx > 50:
            print("End of the test game")
            break
