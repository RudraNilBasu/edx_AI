import time
from BaseAI import BaseAI


MAX_TIME = 0.1
EXTRA_GRACE_TIME = 0.05
debug = {}


class Position:
    def __init__(self, positionGrid, move=None, theDepth=0):
        self.positionGrid = positionGrid
        self.positionMove = move
        self.positionDepth = theDepth

    def getAllNeighbours(self, isMaximum=True):
        neighbours = []

        if isMaximum:
            availableMoves = self.positionGrid.getAvailableMoves()
            for perMove in availableMoves:
                new_grid = self.positionGrid.clone()
                new_grid.move(perMove)
                neighbours.append(Position(new_grid, perMove, self.positionDepth + 1))
            neighbours.sort(key=evalFun, reverse=True)
        else:
            availableCells = self.positionGrid.getAvailableCells()
            if len(availableCells) > 0:
                for perCell in self.positionGrid.getAvailableCells():
                    new_grid = self.positionGrid.clone()
                    new_grid.setCellValue(perCell, 2)
                    neighbours.append(Position(new_grid, self.positionMove, self.positionDepth + 1))
                    new_grid = self.positionGrid.clone()
                    new_grid.setCellValue(perCell, 4)
                    neighbours.append(Position(new_grid, self.positionMove, self.positionDepth + 1))

            neighbours.sort(key=evalFun)
        return neighbours

    def __eq__(self, other):
        """
        """
        for eachRow in xrange(self.positionGrid.size):
            if self.positionGrid.map[eachRow] != other.grid.map[eachRow]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.positionGrid.map))


def evalFun(position):
    maxTile = position.positionGrid.getMaxTile()
    totalAvailableCells = len(position.positionGrid.getAvailableCells())


    r = 0.25
    calculation1 = position.positionGrid.map[3][0] + position.positionGrid.map[3][1] * r
    calculation1 += position.positionGrid.map[3][2] * r ** 2 + position.positionGrid.map[3][3] * r ** 3
    calculation1 += position.positionGrid.map[2][3] * r ** 4 + position.positionGrid.map[2][2] * r ** 5 + position.positionGrid.map[2][1] * r ** 6
    calculation1 += position.positionGrid.map[2][0] * r ** 7 + position.positionGrid.map[1][0] * r ** 8 + position.positionGrid.map[1][1] * r ** 9
    calculation1 += position.positionGrid.map[1][2] * r ** 10 + position.positionGrid.map[1][3] * r ** 11 + position.positionGrid.map[0][3] * r ** 12
    calculation1 += position.positionGrid.map[0][2] * r ** 13 + position.positionGrid.map[0][1] * r ** 14 + position.positionGrid.map[0][0] * r ** 15

    calculation2 = position.positionGrid.map[3][0] + position.positionGrid.map[2][0] * r
    calculation2 += position.positionGrid.map[1][0] * r ** 2 + position.positionGrid.map[0][0] * r ** 3
    calculation2 += position.positionGrid.map[0][1] * r ** 4 + position.positionGrid.map[1][1] * r ** 5 + position.positionGrid.map[2][1] * r ** 6
    calculation2 += position.positionGrid.map[3][1] * r ** 7 + position.positionGrid.map[3][2] * r ** 8 + position.positionGrid.map[2][2] * r ** 9
    calculation2 += position.positionGrid.map[1][2] * r ** 10 + position.positionGrid.map[0][2] * r ** 11 + position.positionGrid.map[0][3] * r ** 12
    calculation2 += position.positionGrid.map[1][3] * r ** 13 + position.positionGrid.map[2][3] * r ** 14 + position.positionGrid.map[3][3] * r ** 15
    return maxTile + 10 * max(calculation1, calculation2) + 3 * totalAvailableCells


class EndRunTimeException(Exception):
    pass


def minimize(position, alpha, beta, maxDepth):
    global initial_time
    runningTime = time.clock() - initial_time

    # commenting for debug
    if runningTime >= MAX_TIME:
        raise (EndRunTimeException('Ending the process'))

    allPossibleNeighbours = position.getAllNeighbours(False)
    process_Test = False
    if len(allPossibleNeighbours) == 0:
        process_Test = True
    else:
        process_Test = False
    if position.positionDepth > maxDepth or runningTime > MAX_TIME + EXTRA_GRACE_TIME or process_Test:
        return (None, evalFun(position))

    (minChild, minUtility) = (None, float('Inf'))

    for neighbour in allPossibleNeighbours:
        (_, utility) = maximize(neighbour, alpha, beta, maxDepth)

        if utility < minUtility:
            (minChild, minUtility) = (neighbour, utility)

        if minUtility <= alpha:
            break

        if minUtility < beta:
            beta = minUtility

    return (minChild, minUtility)


def maximize(position, alpha, beta, maxDepth):
    global initial_time, runningTime
    runningTime = time.clock() - initial_time

    # commenting for project debug
    if runningTime >= MAX_TIME:
        raise (EndRunTimeException('Ending the process'))

    allPossibleNeighbours = position.getAllNeighbours()
    process_Test = False
    if len(allPossibleNeighbours) == 0:
        process_Test = True
    else:
        process_Test = False
    if position.positionDepth > maxDepth or process_Test:
        return (None, evalFun(position))

    (maxChild, maxUtility) = (None, float('-Inf'))

    for neighbour in allPossibleNeighbours:
        (_, utility) = minimize(neighbour, alpha, beta, maxDepth)

        if utility > maxUtility:
            (maxChild, maxUtility) = (neighbour, utility)

        if maxUtility >= beta:
            break

        if maxUtility > alpha:
            alpha = maxUtility

    return (maxChild, maxUtility)


def utilityFunctionBrain(position, maxDepth):

    global initial_time

    (child, _) = maximize(position, float('-Inf'), float('Inf'), maxDepth)

    return child


class PlayerAI(BaseAI):
    def getMove(self, grid):

        global initial_time, runningTime
        initial_time = time.clock()

        depth = 1
        initialPosition = Position(grid)
        finalPosition = utilityFunctionBrain(initialPosition, depth)
        while True:
            depth += 1
            try:
                updatePosition = utilityFunctionBrain(initialPosition, depth)
            except EndRunTimeException:
                break

            finalPosition = updatePosition

        return finalPosition.positionMove


# Test client, for testing the grid
if __name__ == '__main__':
    from Grid import Grid

    grid = Grid()
    grid.map = [[2, 8, 4, 2], [8, 16, 512, 512], [256, 64, 16, 8], [2, 16, 8, 2]]

    playerAI = PlayerAI()
    print playerAI.getMove(grid)
