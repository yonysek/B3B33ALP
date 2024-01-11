import base as Base
import copy, random


# TODO If there is a move that is next to enemy queen it's a good move. Opposite for my queen.
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

    def fixUpper(self, animal):
        if self.isUpper:
            return animal.upper()
        else:
            return animal.lower()

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
                    if self.board[p][q][-1].isupper() == self.isUpper:
                        result.append([p, q])
        return result

    def move(self):
        if self.start():
            return self.startingMove()

        if self.myMove == 1:
            p, q = self.randomlyPlace()
            if self.myPieces[self.fixUpper("q")] == 0:
                return [self.getRandomPiece(), None, None, p, q]
            return [self.fixUpper("q"), None, None, p, q]

        if self.myMove == 2:
            p, q = self.randomlyPlace()
            if self.myPieces[self.fixUpper("a")] == 0:
                return [self.getRandomPiece(), None, None, p, q]
            return [self.fixUpper("a"), None, None, p, q]

        random = self.random()

        if random is None:
            return []

        animal, p, q, newP, newQ = self.random()

        return [animal, p, q, newP, newQ]

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
            p, q = self.getAllNonemptyCells()[0]
            rand = self.direction[random.randint(0, 5)]
            return [self.fixUpper("g"), None, None, p + rand[0], q + rand[1]]
            # return [self.fixUpper("g"), None, None, 2, 7]

    def getRandomPiece(self):
        availableAnimals = [i for i in self.myPieces if self.myPieces[i] > 0]
        if len(availableAnimals) == 0:
            return False
        animal = availableAnimals[random.randint(0, len(availableAnimals) - 1)]
        return animal

    def validPlacement(self, p, q):
        if not self.isEmpty(p, q, self.board) or not self.inBoard(p, q):
            return False

        numOfAllies = 0
        for i in range(6):
            newP = p + self.direction[i][0]
            newQ = q + self.direction[i][1]
            if not self.inBoard(newP, newQ):
                continue
            if self.board[newP][newQ] in self.allies:
                numOfAllies += 1
            if self.board[newP][newQ] in self.enemies:
                return False

            if len(self.board[newP][newQ]) > 1:
                for i in self.board[newP][newQ]:
                    if i in self.enemies:
                        return False

        if numOfAllies > 0:
            return True

    def randomlyPlace(self):
        placements = [
            [p, q]
            for p in self.board
            for q in self.board[p]
            if self.validPlacement(p, q)
        ]
        if len(placements) == 0:
            return None, None
        randomPlacement = placements[random.randint(0, len(placements) - 1)]
        return randomPlacement

    def surroundings(self, board, p, q):
        o = [0] * 6
        for i in range(6):
            if self.inBoard(p + self.direction[i][0], q + self.direction[i][1]):
                pos = [p + self.direction[i][0], q + self.direction[i][1]]
                o[i] = pos
            else:
                o[i] = -1

        surroundings = o

        return surroundings

    def neighbours(self, board, p, q):
        surroundings = self.surroundings(board, p, q)
        neighbours = []
        for k in surroundings:
            if k == -1:
                continue
            pos = board[k[0]][k[1]]
            if pos != "":
                pos = pos[-1]
            if pos in self.enemies or pos in self.allies:
                neighbours.append([k[0], k[1]])
        return neighbours

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
                if board[p][q] != "":
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

    def willBreakHive(self, p, q, newP, newQ):
        testBoard = copy.deepcopy(self.board)

        animal = testBoard[p][q][-1]
        testBoard[p][q] = testBoard[p][q][:-1]

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

    def checkMoves(self, p, q, moves):
        checkedMoves = []
        for i in moves:
            if not self.inBoard(i[0], i[1]):
                continue

            if not self.willBreakHive(p, q, i[0], i[1]):
                checkedMoves.append(i)
        return checkedMoves

    def asqMove(self, p, q, board):
        o = [0] * 6

        for i in range(6):
            if self.inBoard(p + self.direction[i][0], q + self.direction[i][1]):
                if (q + self.direction[i][1]) in board[p + self.direction[i][0]]:
                    pos = board[p + self.direction[i][0]][q + self.direction[i][1]]
                    if pos != "":
                        pos = pos[-1]
                    if pos in self.enemies or pos in self.allies:
                        o[i] = 1
                    else:
                        o[i] = 0
            else:
                o[i] = -1

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

    def posPos(self, p, q, n):
        board = copy.deepcopy(self.board)
        o_p, o_q = p, q

        pos = [[p, q]]

        dontGoBack = pos[:]
        board[p][q] = ""

        for i in range(n):
            pos2 = []
            for p, q in pos:
                possible = self.asqMove(p, q, board)
                for x in possible:
                    if x not in dontGoBack:
                        pos2.append(x)
                        dontGoBack.append(x)
                    else:
                        pass

            pos = pos2[:]

        posPos = self.checkMoves(o_p, o_q, pos2)

        return posPos

    def getValidMoves(self, p, q):
        animal = self.board[p][q][-1].lower()
        moves = []

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

            for j in addition:
                if j not in moves:
                    moves.append(j)
            n += 1

        return moves

    def getValidMovesBeetle(self, p, q):
        o = self.surroundings(self.board, p, q)

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
            p_dir = p + self.direction[i][0]
            q_dir = q + self.direction[i][1]
            if not self.inBoard(p_dir, q_dir):
                continue
            if self.board[p_dir][q_dir] != "":
                while True:
                    new_p += self.direction[i][0]
                    new_q += self.direction[i][1]
                    if not self.inBoard(new_p, new_q):
                        break
                    if self.board[new_p][new_q] == "":
                        moves.append([new_p, new_q])
                        break

        moves = self.checkMoves(p, q, moves)

        return moves

    def findQueen(self):
        animal = "q"
        if self.isUpper:
            animal = animal.lower()
        else:
            animal = animal.upper()

        for p in self.board:
            for q in self.board[p]:
                if animal in self.board[p][q]:
                    return p, q

        return None, None

    def valueTiles(self, p, q, depth=0, values={}, direction=0, org=True):
        if values == {}:
            values = copy.deepcopy(self.board)
            for i in values:
                for j in values[i]:
                    values[i][j] = -1

            values[p][q] = 0
            for i in range(6):
                p1 = p + self.direction[i][0]
                q1 = q + self.direction[i][1]
                self.valueTiles(p1, q1, depth + 1, values, i, True)

            return values

        if not self.inBoard(p, q):
            return

        values[p][q] = depth

        dir1 = self.direction[direction % 6]
        dir2 = self.direction[(direction + 1) % 6]
        p1 = p + dir1[0]
        q1 = q + dir1[1]

        p2 = p + dir2[0]
        q2 = q + dir2[1]

        self.valueTiles(p1, q1, depth + 1, values, direction, org)

        if org:
            self.valueTiles(p2, q2, depth + 1, values, direction + 1, False)

    def devalueAroundQueen(self, values):
        animal = "q"
        if self.isUpper:
            animal = animal.upper()
        else:
            animal = animal.lower()

        queenP, queenQ = None, None

        for p in self.board:
            for q in self.board[p]:
                if animal in self.board[p][q]:
                    queenP, queenQ = p, q

        p, q = queenP, queenQ

        numOfNeighbours = 0
        for i in range(6):
            p1 = p + self.direction[i][0]
            q1 = q + self.direction[i][1]
            if self.inBoard(p1, q1):
                if self.board[p1][q1] != "":
                    numOfNeighbours += 1

        if p is None or q is None:
            return values

        for i in range(6):
            p1 = p + self.direction[i][0]
            q1 = q + self.direction[i][1]
            if self.inBoard(p1, q1):
                values[p1][q1] += numOfNeighbours + 1

        return values

    def asignValue(self, animal):
        animal = animal.lower()
        value = 0
        if animal == "a":
            value = 3
        elif animal == "b":
            value = 8
        elif animal == "s":
            value = 7
        elif animal == "g":
            value = 5

        return value

    def getBestMove(self, moves):
        bestMove = []
        pQ, qQ = self.findQueen()
        if pQ is None or qQ is None:
            return bestMove
        tileValues = self.valueTiles(pQ, qQ)
        tileValues = self.devalueAroundQueen(tileValues)
        bestValue = -1
        print(tileValues)
        for i in moves:
            if type(i) is str:
                p, q = None, None
            else:
                p, q = i

            if p is not None:
                value = tileValues[p][q]
                if self.board[p][q][-1] == "Q" or self.board[p][q][-1] == "q":
                    value += 10
                if value in [0, 1]:
                    continue
            else:
                value = self.asignValue(i)

            curMoves = moves[i]
            for j in curMoves:
                newP, newQ = j
                newValue = tileValues[newP][newQ]
                delta = value - newValue
                absDelta = delta
                print(i, j, delta, absDelta)
                if absDelta > bestValue:
                    bestValue = absDelta
                    bestMove = [p, q, newP, newQ, i]

        return bestMove

    def allPlacements(self):
        placements = {}

        for i in self.myPieces:
            if self.myPieces[i] == 0:
                continue
            placements[i] = []
            for p in self.board:
                for q in self.board[p]:
                    if self.validPlacement(p, q):
                        placements[i].append([p, q])
        return placements

    def randomAvailableAnimal(self):
        availableAnimals = [i for i in self.myPieces if self.myPieces[i] > 0]
        if len(availableAnimals) == 0:
            return False
        animal = availableAnimals[random.randint(0, len(availableAnimals) - 1)]
        return animal

    def random(self):
        # type = None

        placements = self.allPlacements()

        allMyCells = self.getAllMyCells()
        moves = {}
        for i in range(len(allMyCells)):
            p, q = allMyCells[i]
            move = self.getValidMoves(p, q)
            moves[(p, q)] = move

        allMoves = moves.copy()
        allMoves.update(placements)

        if self.myMove in [3]:
            animal = self.getRandomPiece()
            p, q = self.randomlyPlace()
            return [animal, None, None, p, q]

        # if type == "move":
        bestMove = self.getBestMove(allMoves)
        if len(bestMove) != 0:
            if bestMove[0] is None and bestMove[1] is None:
                return [
                    bestMove[4],
                    None,
                    None,
                    bestMove[2],
                    bestMove[3],
                ]
            return [
                self.board[bestMove[0]][bestMove[1]][-1],
                bestMove[0],
                bestMove[1],
                bestMove[2],
                bestMove[3],
            ]

        for i in moves:
            if len(moves[i]) != 0:
                p, q = i
                break

        if len(moves[(p, q)]) == 0:
            return None
        newP, newQ = moves[i][random.randint(0, len(moves[(p, q)]) - 1)]
        animal = self.board[p][q][-1]
        return [animal, p, q, newP, newQ]


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
        with open("failed_board.txt", "w") as file:
            file.write(f"{P1.board}")
        # print(P1.board)
        move = P1.move()
        # print(moveIdx, "P1 returned", move)
        updatePlayers(move, P1, P2)  # update P1 and P2 according to the move
        filename = "moves/move-{:03d}-player1.png".format(moveIdx)
        # filename = "progress.png"
        # P1.saveImage(filename)
        # time.sleep(0.5)

        # print(P2.board)
        move = P2.move()
        # print(moveIdx, "P2 returned", move)
        updatePlayers(move, P2, P1)  # update P2 and P1 according to the move
        filename = "moves/move-{:03d}-player2.png".format(moveIdx)
        # P1.saveImage(filename)
        # time.sleep(0.5)

        moveIdx += 1
        P1.myMove = moveIdx
        P2.myMove = moveIdx

        # print(P1.myPieces)
        # print(P2.myPieces)

        if moveIdx > 50:
            print("End of the test game")
            break
