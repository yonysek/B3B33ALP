import sys
import copy

s = 69
if s == 0:
    with open(
        "/Users/yonysek/Library/CloudStorage/GoogleDrive-vybirjon@fel.cvut.cz/My Drive/Winter 2023:24/B3B33ALP/Homeworks/10/board.txt",
        "r",
    ) as file:
        board = file.read()
else:
    board = open(sys.argv[1], "rt")
    board = board.read()


# DOWN RIGHT UP LEFT
directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

diagonals = ((-1, 1), (-1, -1), (1, -1), (1, 1))


def changeBoardBack(board):
    boardList = board
    for i in range(len(boardList)):
        for j in range(len(boardList[i])):
            if boardList[i][j] > 0:
                boardList[i][j] = int(str(boardList[i][j]).split(".")[0])

    return boardList


def printBoard(board):
    somethingUnrelated = copy.deepcopy(board)
    somethingUnrelated = changeBoardBack(somethingUnrelated)
    for i in somethingUnrelated:
        print(i)
    print("\n")


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


# Throwaway function to create dictionary of islands that will be used to keep track of their sizes and coordinates
def createIslands(board):
    islands = {}

    boardList = board

    for i in range(len(boardList)):
        for j in range(len(boardList)):
            el = boardList[i][j]
            appendix = 0
            keysIs = list(islands.keys())
            for k in range(len(keysIs), 0, -1):
                k = k - 1
                key = int(str(keysIs[k]).split(".")[0])
                keyAppendix = int(str(keysIs[k]).split(".")[1])
                if el == key:
                    appendix = keyAppendix + 1
                    break
            if el not in [-1, 0]:
                el = float(f"{str(el)}.{appendix}")
                islands[el] = [(i, j)]

    return islands


global islands
islands = createIslands(board)


# Creates unique islands
def changeBoard(board):
    boardList = board
    for k in islands:
        i, j = islands[k][0]
        boardList[i][j] = k

    return boardList


board = changeBoard(board)


def islandsFromBoard(board):
    islands = {}

    for i in range(len(board)):
        for j in range(len(board)):
            el = board[i][j]
            if el not in [-1, 0]:
                if el not in islands:
                    islands[el] = [(i, j)]
                else:
                    islands[el].append((i, j))

    return islands


# Gets back the number of the island therefore the size
def getElNum(board, i, j):
    if board[i][j] > 0:
        return int(str(board[i][j]).split(".")[0])
    else:
        return board[i][j]


# Gets the current size of the island
def getSize(board, i, j):
    size = len(islands[board[i][j]])
    return size


# Checks if position is in board
def inBoard(board, i, j):
    if i < 0 or j < 0 or i > len(board) - 1 or j > len(board) - 1:
        return False
    else:
        return True


def islandSurroundings(board, island):
    surroundings = []
    for tile in islands[island]:
        i, j = tile
        for direction in directions:
            iC = i + direction[0]
            jC = j + direction[1]
            if not inBoard(board, iC, jC):
                continue
            if board[iC][jC] != island:
                surroundings.append((iC, jC))

    return surroundings


def islandSurroundings(board, island):
    surroundings = []
    for tile in islands[island]:
        i, j = tile
        for direction in directions:
            iC = i + direction[0]
            jC = j + direction[1]
            if not inBoard(board, iC, jC):
                continue
            if board[iC][jC] != island:
                surroundings.append((iC, jC))

    return surroundings


def markAroundFinishedIslands(board, check=False):
    oldBoard = copy.deepcopy(board)

    for island in islands:
        if len(islands[island]) == int(str(island).split(".")[0]):
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
    reachableTiles = [[i, j]]

    # Finds the number of remaining tiles to be added to the island
    for k in range(d, 0, -1):
        for iC in range(len(board)):
            for jC in range(len(board)):
                if distance(board, i, j, iC, jC) == k:
                    reachableTiles.append([iC, jC])
    return reachableTiles


# Self explanatory
def markUnreachableTiles(board, check=False):
    oldBoard = copy.deepcopy(board)

    availableTiles = []
    islands = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] > 0:
                islands.append([i, j])
    for k in islands:
        i, j = k
        availableTiles.extend(reachableTiles(board, i, j))

    for i in range(len(board)):
        for j in range(len(board)):
            if [i, j] not in availableTiles:
                board[i][j] = 0

    if check and oldBoard != board:
        print("markUnreachableTiles")
        printBoard(board)


def reachableTiles(board):
    reachableTiles = []

    for island in islands:
        desiredSize = int(str(island).split(".")[0])
        actualSize = len(islands[island])
        d = desiredSize - actualSize

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
            if [i, j] not in tiles:
                unreachableTiles.append([i, j])

    for i in range(len(board)):
        for j in range(len(board)):
            if [i, j] in unreachableTiles:
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
                stack.append([i, j])
                while len(stack) > 0:
                    current.append(stack.pop())
                    for k in directions:
                        iC = current[-1][0] + k[0]
                        jC = current[-1][1] + k[1]
                        if not inBoard(board, iC, jC):
                            continue
                        if board[iC][jC] == 0 and [iC, jC] not in current:
                            stack.append([iC, jC])
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
# This will need improvement because it will not expand every time it needs to (think I fixed it?)
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


# Gives possible expansions of an island
def possibleExpansions(board, island):
    possibleExpansions = []
    if len(islands[island]) == int(str(island).split(".")[0]):
        return possibleExpansions

    surroundings = islandSurroundings(board, island)

    for tile in surroundings:
        i, j = tile
        if board[i][j] == -1:
            possibleExpansions.append(tile)

    return possibleExpansions


# Gives all possible expansions of all islands
def allPossibleExpansions(board):
    allPossibleExpansions = {}
    for island in islands:
        if island not in allPossibleExpansions:
            allPossibleExpansions[island] = []

        allPossibleExpansions[island].extend((possibleExpansions(board, island)))

    return allPossibleExpansions


def expandDefiniteIslands(board, check=False):
    oldBoard = copy.deepcopy(board)

    posExp = allPossibleExpansions(board)
    for island in posExp:
        if len(posExp[island]) == 1:
            i, j = posExp[island][0]
            board[i][j] = island
            islands[island].append((i, j))

    if check and oldBoard != board:
        print("expandDefiniteIslands")
        printBoard(board)


def passiveGameLoop(board):
    changingBoard = copy.deepcopy(board)
    while True:
        markAroundFinishedIslands(board, True)
        markUnreachableTiles(board, True)
        markInterspace(board, True)
        markDiagonals(board, True)
        expandRivers(board, True)
        expandDefiniteIslands(board, True)
        if changingBoard == board:
            break
        changingBoard = copy.deepcopy(board)


def pools(board):
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
                return True


def isolatedRiver(board):
    rivers = findRivers(board)
    if len(rivers) == 1:
        return
    validRivers = 0
    for river in rivers:
        expansions = 0
        for tile in river:
            for direction in directions:
                iC = tile[0] + direction[0]
                jC = tile[1] + direction[1]
                if not inBoard(board, iC, jC):
                    continue
                if board[iC][jC] == 0:
                    continue
                if board[iC][jC] == -1:
                    expansions += 1
        if expansions > 0:
            validRivers += 1

    if validRivers == len(rivers):
        return False

    return True


def isolatedIsland(board):
    for island in islands:
        surroundings = islandSurroundings(board, island)
        expandableSurroundings = []
        for tile in surroundings:
            i, j = tile
            if board[i][j] == -1:
                expandableSurroundings.append(tile)

        if (
            len(islands[island]) != int(str(island).split(".")[0])
            and len(expandableSurroundings) == 0
        ):
            return True

    return False


def notEnoughSpace(board):
    remainingToExpand = 0
    for island in islands:
        remainingToExpand += int(str(island).split(".")[0]) - len(islands[island])

    notFilled = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == -1:
                notFilled += 1

    if remainingToExpand > notFilled:
        return True

    return False


def rules(board):
    if (
        pools(board)
        or isolatedRiver(board)
        or isolatedIsland(board)
        or notEnoughSpace(board)
    ):
        return False

    return True


def rules(board):
    if pools(board):
        print("pools")
        return False
    if isolatedRiver(board):
        print("isolatedRiver")
        return False
    if isolatedIsland(board):
        print("isolatedIsland")
        return False
    if notEnoughSpace(board):
        print("notEnoughSpace")
        return False

    return True


# Expands an island to the given coordinates and adds them to the islands
def expandIsland(board, island, coords):
    iC = coords[0]
    jC = coords[1]
    board[iC][jC] = island
    islands[island].append((iC, jC))


global stepId
global stepDict
global triedSteps
stepId = 0
stepDict = {}
triedSteps = {}


def printOnlyPossibleExpansions():
    onlyPosExp = {}
    for i in stepDict:
        onlyPosExp[i] = stepDict[i]["posExp"]

    for i in onlyPosExp:
        print(i, onlyPosExp[i])


def saveStep(board, isles, posExp):
    global stepId
    stepId += 1
    entry = {}
    entry["board"] = copy.deepcopy(board)
    entry["islands"] = copy.deepcopy(isles)
    entry["posExp"] = copy.deepcopy(posExp)
    for step in triedSteps:
        if triedSteps[step] == entry:
            stepId -= 1
            return False

    triedSteps[stepId] = entry
    stepDict[stepId] = entry


def updateIslands(newIslands):
    global islands
    islands = copy.deepcopy(newIslands)


def doStep():
    global stepId
    newBoard = copy.deepcopy(stepDict[stepId]["board"])
    # newIslands = copy.deepcopy(stepDict[stepId]["islands"])
    newIslands = islandsFromBoard(newBoard)
    posExp = stepDict[stepId]["posExp"]

    island = None
    expansion = []
    for exp in posExp:
        if posExp[exp] != []:
            island = exp
            expansion = posExp[exp].pop(0)
            break

    if island is None:
        undoStep()
        return

    print("Before expanding")
    printBoard(newBoard)

    i, j = expansion
    newBoard[i][j] = island
    newIslands[island].append((i, j))

    updateIslands(newIslands)

    print("Expanding", island, "to", expansion)
    printBoard(newBoard)

    passiveGameLoop(newBoard)

    print("After passive game loop")
    printBoard(newBoard)

    if not rules(newBoard):
        # undoStep()
        return

    saveStep(newBoard, newIslands, allPossibleExpansions(newBoard))


def undoStep():
    global stepId
    # print("Undoing step")
    stepDict.pop(stepId)
    stepId -= 1
    print("backing to")
    printBoard(stepDict[stepId]["board"])


def activeGameLoop():
    global finalBoard
    posExp = allPossibleExpansions(board)
    # Sort the dictionary by the length of its elements
    posExp = dict(sorted(posExp.items(), key=lambda x: len(x[1])))
    saveStep(board, islands, posExp)

    s = 0
    while s < 1000000:
        doStep()
        boardToCheck = stepDict[stepId]["board"]

        if gameOver(boardToCheck):
            finalBoard = boardToCheck
            break

        s += 1


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


print("Initial board")
printBoard(board)
passiveGameLoop(board)
print("After passive game loop")
printBoard(board)

# quit()

activeGameLoop()


board = changeBoardBack(finalBoard)
# printBoard(board)
for i in range(len(board)):
    print(" ".join(str(x) for x in board[i]))
