# THIRD TIME THE CHARM
import sys
import copy

sys.setrecursionlimit(5000)

s = 0
if s == 0:
    with open(
        "/Users/yonysek/Library/CloudStorage/GoogleDrive-vybirjon@fel.cvut.cz/My Drive/Winter 2023:24/B3B33ALP/Homeworks/10/board.txt",
        "r",
    ) as file:
        board = file.read()
else:
    board = open(sys.argv[1], "rt")
    board = board.read()

board = board.split("\n")


boardList = []
for i in board:
    if "" == i:
        continue
    temp = []
    i = i.strip().split(" ")
    for j in range(len(i)):
        if i[j] == "":
            continue
        temp.append(int(i[j]))
    boardList.append(temp)

board = boardList

# DOWN RIGHT UP LEFT
directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

diagonals = ((-1, 1), (-1, -1), (1, -1), (1, 1))


# Prints board in a nice way
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


def islandInBoard(board, island):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == island:
                return True
    return False


def getUniqueNumber(board, num):
    dec = 0
    while True:
        island = float(f"{num}.{dec}")
        if not islandInBoard(board, island):
            return island
        dec += 1


def changeBoard():
    newBoard = copy.deepcopy(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            tile = board[i][j]
            if tile > 0:
                newBoard[i][j] = getUniqueNumber(newBoard, tile)

    return newBoard


board = changeBoard()
# printBoard(board)


# Creates islands dictionary based on given board
def createIslands(board):
    islands = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            tile = board[i][j]
            if tile > 0:
                if tile not in islands:
                    islands[tile] = []
                islands[tile].append((i, j))
    return islands


islands = createIslands(board)


# Checks if position is in board
def inBoard(board, i, j):
    if i < 0 or j < 0 or i > len(board) - 1 or j > len(board) - 1:
        return False
    else:
        return True


# Gets back the number of the island therefore the desired size
def getOriginalIsland(island):
    return int(str(island).split(".")[0])


def printFinalBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                board[i][j] = getOriginalIsland(board[i][j])

    for i in range(len(board)):
        print(" ".join(str(x) for x in board[i]))


# Gets the current size of the island
def getSize(board, island):
    size = len(islands[island])
    return size


def islandSurroundings(board, island):
    surroundings = []
    for tile in islands[island]:
        i, j = tile
        for direction in directions:
            iC = i + direction[0]
            jC = j + direction[1]
            if not inBoard(board, iC, jC):
                continue
            if board[iC][jC] != island and (iC, jC) not in surroundings:
                surroundings.append((iC, jC))

    return surroundings


def isIslandFinished(board, island):
    size = getSize(board, island)
    desiredSize = getOriginalIsland(island)
    if size == desiredSize:
        return True
    else:
        return False


# Takes the list of islands and if the island is finished then marks the surroundings
def markAroundFinishedIslands(board, check=False):
    oldBoard = copy.deepcopy(board)

    for island in islands:
        if isIslandFinished(board, island):
            surroundings = islandSurroundings(board, island)
            for tile in surroundings:
                i, j = tile
                if board[i][j] == -1:
                    board[i][j] = 0
    if check and oldBoard != board:
        print("markAroundFinishedIslands")
        printBoard(board)


def distance(board, i, j, toI, toJ):
    distance = abs(toI - i) + abs(toJ - j)
    return distance


# Finds the reachable tiles from an island based on its size
def reachableTilesFromPosition(board, i, j, d):
    reachableTiles = [(i, j)]

    # Finds the number of remaining tiles to be added to the island
    for k in range(d, 0, -1):
        for iC in range(len(board)):
            for jC in range(len(board)):
                if distance(board, i, j, iC, jC) == k:
                    reachableTiles.append((iC, jC))
    return reachableTiles


def reachableTiles(board):
    reachableTiles = []

    for island in islands:
        desiredSize = int(str(island).split(".")[0])
        size = len(islands[island])
        d = desiredSize - size

        for tile in islands[island]:
            i, j = tile
            reachableTiles.extend(reachableTilesFromPosition(board, i, j, d))

    return reachableTiles


def markUnreachableTiles(board, check=False):
    oldBoard = copy.deepcopy(board)

    tiles = reachableTiles(board)
    unreachableTiles = []
    for i in range(len(board)):
        for j in range(len(board)):
            if (i, j) not in tiles:
                unreachableTiles.append((i, j))

    for i in range(len(board)):
        for j in range(len(board)):
            if (i, j) in unreachableTiles:
                board[i][j] = 0

    if check and oldBoard != board:
        print("markUnreachableTiles")
        printBoard(board)


# Marks the tiles between islands
def markInterspace(board, check=False):
    oldBoard = copy.deepcopy(board)

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] > 0:
                for k in range(len(directions)):
                    iC = i + 2 * directions[k][0]
                    jC = j + 2 * directions[k][1]
                    if not inBoard(board, iC, jC):
                        continue
                    interspace = board[i + directions[k][0]][j + directions[k][1]]
                    if board[iC][jC] > 0 and interspace != board[i][j]:
                        board[i + directions[k][0]][j + directions[k][1]] = 0
    if check and oldBoard != board:
        print("markInterspace")
        printBoard(board)


# Marks the tiles between islands diagonally
def markDiagonals(board, check=False):
    oldBoard = copy.deepcopy(board)

    for i in range(len(board)):
        for j in range(len(board)):
            tile = board[i][j]
            if tile > 0:
                for k in diagonals:
                    iC = i + k[0]
                    jC = j + k[1]
                    if not inBoard(board, iC, jC):
                        continue
                    checkTile = board[iC][jC]
                    if checkTile > 1 and checkTile != tile:
                        board[i + k[0]][j] = 0
                        board[i][j + k[1]] = 0
    if check and oldBoard != board:
        print("markDiagonals")
        printBoard(board)


def findRivers(board):
    rivers = []
    for i in range(len(board)):
        for j in range(len(board)):
            current = []
            stack = []
            if board[i][j] == 0:
                stack.append((i, j))
                while len(stack) > 0:
                    current.append(stack.pop())
                    for k in directions:
                        iC = current[-1][0] + k[0]
                        jC = current[-1][1] + k[1]
                        if not inBoard(board, iC, jC):
                            continue
                        if board[iC][jC] == 0 and (iC, jC) not in current:
                            stack.append((iC, jC))
                if len(rivers) == 0:
                    rivers.append(current)
                unique = True
                for river in rivers:
                    if len(current) == len(river):
                        for tile in current:
                            if tile in river:
                                unique = False
                                continue

                if unique:
                    rivers.append(current)

    return rivers


# If a river has only one possible expansion, expand it
def expandRivers(board, check=False):
    oldBoard = copy.deepcopy(board)

    rivers = findRivers(board)
    if len(rivers) == 1:
        return

    placesToExpand = []

    for river in rivers:
        possibleExpansions = []
        for tile in river:
            for direction in directions:
                iC = tile[0] + direction[0]
                jC = tile[1] + direction[1]
                if not inBoard(board, iC, jC):
                    continue

                if board[iC][jC] == -1:
                    possibleExpansions.append([iC, jC])

        if len(possibleExpansions) == 1:
            # i, j = possibleExpansions[0]
            # board[i][j] = 0
            placesToExpand.extend(possibleExpansions)

    for i, j in placesToExpand:
        board[i][j] = 0

    if check and oldBoard != board:
        print("expandRivers")
        printBoard(board)


def expandDefiniteIslands(board, check=False):
    oldBoard = copy.deepcopy(board)

    possibleExpansions = {}
    for island in islands:
        possibleExpansionsForIsland = []
        surroundings = islandSurroundings(board, island)
        if getOriginalIsland(island) == 1:
            continue
        for tile in surroundings:
            i, j = tile
            if board[i][j] == -1:
                possibleExpansionsForIsland.append(tile)

        if len(possibleExpansionsForIsland) == 1:
            possibleExpansions[island] = possibleExpansionsForIsland

    for island in possibleExpansions:
        i, j = possibleExpansions[island][0]
        board[i][j] = island
        islands[island].append((i, j))

    if check and oldBoard != board:
        print("expandDefiniteIslands")
        printBoard(board)


def passiveGameLoop(board, check=False):
    while True:
        oldBoard = copy.deepcopy(board)
        markAroundFinishedIslands(board, check)
        markUnreachableTiles(board, check)
        markInterspace(board, check)
        markDiagonals(board, check)
        expandRivers(board, check)
        expandDefiniteIslands(board, check)

        if oldBoard == board:
            break

    return board


# Need to do rules before getting to possible expansions of islands


def pools(board, check=False):
    poolDirection = ((0, 0), (1, 0), (0, 1), (1, 1))
    for i in range(len(board)):
        for j in range(len(board)):
            riverTiles = 0
            for k in poolDirection:
                iC = i + k[0]
                jC = j + k[1]
                if not inBoard(board, iC, jC):
                    continue
                if board[iC][jC] == 0:
                    riverTiles += 1
            if riverTiles == 4:
                if check:
                    print("pools")
                return True
    return False


def isolatedRiver(board, check=False):
    rivers = findRivers(board)
    if len(rivers) <= 1:
        return False
    for river in rivers:
        expansions = 0
        for tile in river:
            for direction in directions:
                iC = tile[0] + direction[0]
                jC = tile[1] + direction[1]
                if not inBoard(board, iC, jC):
                    continue
                if board[iC][jC] == -1:
                    expansions += 1
        if expansions == 0:
            if check:
                print(river, "isolatedRiver")
            return True

    return False


def isolatedIsland(board, check=False):
    for island in islands:
        surroundings = islandSurroundings(board, island)
        expandableSurroundings = []
        for tile in surroundings:
            i, j = tile
            if board[i][j] == -1:
                expandableSurroundings.append(tile)

        if not isIslandFinished(board, island) and len(expandableSurroundings) == 0:
            if check:
                print(island, "isolatedIsland")
            return True

    return False


def notEnoughSpace(board, check=False):
    remainingToExpand = 0
    for island in islands:
        remainingToExpand += int(str(island).split(".")[0]) - len(islands[island])

    notFilled = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == -1:
                notFilled += 1

    if remainingToExpand > notFilled:
        if check:
            print("notEnoughSpace")
        return True

    return False


def rules(board, check=False):
    if check:
        if (
            pools(board, True)
            or isolatedRiver(board, True)
            or isolatedIsland(board, True)
            or notEnoughSpace(board, True)
        ):
            return False
        else:
            return True

    if (
        pools(board)
        or isolatedRiver(board)
        or isolatedIsland(board)
        or notEnoughSpace(board)
    ):
        return False

    return True


# Try posExp and if not valid then don't add
def possibleExpansions(board, island):
    global islands

    possibleExpansions = []
    surroundings = islandSurroundings(board, island)
    if isIslandFinished(board, island):
        return possibleExpansions

    for tile in surroundings:
        i, j = tile
        if board[i][j] == -1:
            possibleExpansions.append(tile)

    checked = []
    for i in range(len(possibleExpansions)):
        iC, jC = possibleExpansions[i]
        tempBoard = copy.deepcopy(board)
        tempBoard[iC][jC] = island
        islandsBackup = copy.deepcopy(islands)
        islands = createIslands(tempBoard)
        tempBoard = passiveGameLoop(tempBoard)
        viable = rules(tempBoard)

        if viable:
            checked.append(possibleExpansions[i])

        islands = islandsBackup

    return checked


# Gives all possible expansions of all islands
def allPossibleExpansions(board):
    allPossibleExpansions = {}
    for island in islands:
        if island not in allPossibleExpansions:
            allPossibleExpansions[island] = []

        allPossibleExpansions[island].extend((possibleExpansions(board, island)))

    return allPossibleExpansions


def OPexpandDefiniteIslands(board, check=False):
    possibleExpansions = allPossibleExpansions(board)

    definiteExpansions = {}
    for island in possibleExpansions:
        if len(possibleExpansions[island]) == 1:
            definiteExpansions[island] = possibleExpansions[island]

    for island in definiteExpansions:
        i, j = definiteExpansions[island][0]
        board[i][j] = island
        islands[island].append((i, j))
        if check:
            print("OPexpandDefiniteIslands")
            printBoard(board)


def OPpassiveGameLoop(board, check=False):
    while True:
        oldBoard = copy.deepcopy(board)
        passiveGameLoop(board, check)
        OPexpandDefiniteIslands(board, check)

        if oldBoard == board:
            break

    return board


OPpassiveGameLoop(board)
# printBoard(board)

# TODO It is now time to do the fucking bullshit which I'm not ready for, therefore me be going to sleep with the wish to never wake up again.


def numberOfExpansions(expansions):
    num = 0
    for i in expansions:
        num += len(expansions[i])
    return num


def doExpansion(board, island, expansion, check=False):
    global islands

    newBoard = copy.deepcopy(board)
    i, j = expansion
    newBoard[i][j] = island
    islandsBackup = copy.deepcopy(islands)
    islands = createIslands(newBoard)
    passiveGameLoop(newBoard, check)
    return newBoard, islandsBackup


# printBoard(board)


def getBestExpansion(board, possibleExpansions):
    global islands

    lowestNewMoves = None
    bestExpansion = {}

    for island in possibleExpansions:
        for exp in possibleExpansions[island]:
            newBoard, islandsBackup = doExpansion(board, island, exp)
            expansions = allPossibleExpansions(newBoard)
            numOfExp = numberOfExpansions(expansions)
            if lowestNewMoves is None:
                lowestNewMoves = numOfExp
                bestExpansion[island] = exp

            if numOfExp < lowestNewMoves:
                lowestNewMoves = numOfExp
                bestExpansion = {}
                bestExpansion[island] = exp

            islands = islandsBackup
    return bestExpansion


def gameOver(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == -1:
                return False

    for island in islands:
        size = int(str(island).split(".")[0])
        if len(islands[island]) != size:
            return False
    return True


def filterExpansions(bestExpansion, possibleExpansions):
    island = list(bestExpansion.keys())[0]
    expansion = bestExpansion[island]

    possibleExpansions[island].remove(expansion)

    return island, expansion


stepDict = {}


def addToStepDict(step, board, islands, possibleExpansions):
    global stepDict

    dict = {}
    dict["board"] = board
    dict["islands"] = islands
    dict["possibleExpansions"] = possibleExpansions

    stepDict[step] = dict


def getFromStepDict(step):
    board = stepDict[step]["board"]
    islands = stepDict[step]["islands"]
    possibleExpansions = stepDict[step]["possibleExpansions"]

    board = copy.deepcopy(board)

    return board, islands, possibleExpansions


triedBoards = []


def activeGameLoop(steps=0):
    global islands
    global triedBoards

    board, islands, posExp = getFromStepDict(steps)

    newBoard = copy.deepcopy(board)

    bestExpansion = getBestExpansion(newBoard, posExp)

    if len(bestExpansion) == 0:
        activeGameLoop(steps - 1)

    # print(
    #     f"step {steps} exp {bestExpansion} posExp {posExp[list(bestExpansion.keys())[0]]}"
    # )
    island, expansion = filterExpansions(bestExpansion, posExp)

    newBoard, islandsBackup = doExpansion(newBoard, island, expansion)

    if newBoard in triedBoards:
        activeGameLoop(steps)

    triedBoards.append(newBoard)

    # print(f"step {steps} exp {bestExpansion} posExp {posExp[island]}")
    # printBoard(newBoard)
    # print(stepDict)

    if gameOver(newBoard):
        printFinalBoard(newBoard)
        quit()

    newPosExp = allPossibleExpansions(newBoard)

    if numberOfExpansions(newPosExp) == 0:
        activeGameLoop(steps)

    steps += 1

    addToStepDict(steps, newBoard, islands, newPosExp)

    activeGameLoop(steps)


if gameOver(board):
    printFinalBoard(board)
    quit()

posExp = allPossibleExpansions(board)

addToStepDict(0, board, islands, posExp)

activeGameLoop()


printFinalBoard(board)
