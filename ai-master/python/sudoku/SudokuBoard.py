from CSP_algo import *

class SudokuBoard:

    def __init__(self, boardInitial):
        self.__unassignedValue = []
        self.sudoKuBoard = {}
        looping = 0
        for row__ in "ABCDEFGHI":
            for __col in "123456789":
                self.sudoKuBoard[row__ + __col] = int(boardInitial[looping])
                if self.sudoKuBoard[row__ + __col] == 0:
                    self.__unassignedValue.append(row__ + __col)
                looping += 1

    def getFindTheFreeCells(self):
        return list(self.__unassignedValue)

    def getCurrentCell(self, variable):
        return self.sudoKuBoard[variable]

    def setTheActiveCell(self, variable, value):
        self.sudoKuBoard[variable] = value

    def getKeys(self):
        return self.sudoKuBoard.keys()
            
    def __str__(self):
        stringValue = ""
        dottedLine = "-------------------------------------\n"
        stringValue += dottedLine
        for __rowVice in "ABCDEFGHI":
            stringValue += "|"
            for __colVice in "123456789":
                if self.sudoKuBoard[__rowVice + __colVice] != 0:
                    stringValue += ("%3d" % self.sudoKuBoard[__rowVice + __colVice]) + "|"
                else:
                    stringValue += ("%3c" % ' ') + "|"
            stringValue += "\n" + dottedLine
        return stringValue

class SudokuBoardCSPAlgo(CSP_Algo):
    def __init__(self, sudoku):
        self.sudoku__ = sudoku
        self.variablesKeys = sudoku.getKeys()
        self.unassigned_variables = sudoku.getFindTheFreeCells()
        self.customDomain = {var: [self.sudoku__.getCurrentCell(var)] if self.sudoku__.getCurrentCell(var) != 0 else [1, 2, 3, 4, 5, 6, 7, 8, 9] for var in self.variablesKeys}
        self.constraintsRules = []
        self.emptyFor = 0

        self.constraintsRules.append(["A1", "A2", "A3", "A4" , "A5" , "A6" , "A7" , "A8" , "A9"])
        self.constraintsRules.append(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"])
        self.constraintsRules.append(["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"])
        self.constraintsRules.append(["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"])
        self.constraintsRules.append(["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"])
        self.constraintsRules.append(["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"])
        self.constraintsRules.append(["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"])
        self.constraintsRules.append(["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"])
        self.constraintsRules.append(["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"])

        self.constraintsRules.append(["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1"])
        self.constraintsRules.append(["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2"])
        self.constraintsRules.append(["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", "I3"])
        self.constraintsRules.append(["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4", "I4"])
        self.constraintsRules.append(["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5"])
        self.constraintsRules.append(["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6", "I6"])
        self.constraintsRules.append(["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7", "I7"])
        self.constraintsRules.append(["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8", "I8"])
        self.constraintsRules.append(["A9", "B9", "C9", "D9", "E9", "F9", "G9", "H9", "I9"])

        self.constraintsRules.append(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"])
        self.constraintsRules.append(["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"])
        self.constraintsRules.append(["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"])
        self.constraintsRules.append(["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"])
        self.constraintsRules.append(["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"])
        self.constraintsRules.append(["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"])
        self.constraintsRules.append(["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"])
        self.constraintsRules.append(["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"])
        self.constraintsRules.append(["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"])

        self.binary_constraintsRules = []
        for cell_V in self.variablesKeys:
            for constraintRulesEach in self.constraintsRules:
                if cell_V in constraintRulesEach:
                    for otherCell_v in constraintRulesEach:
                        if otherCell_v != cell_V:
                            self.binary_constraintsRules.append((cell_V, otherCell_v))

    def getNeighbors__(self, X__, restriction__rules=None):
        neighbors_Temp = []
        for arc_eachIterate in self.binary_constraintsRules:
            if X__ == arc_eachIterate[0]:
                if not restriction__rules is None:
                    if restriction__rules != arc_eachIterate[1]:
                        neighbors_Temp.append(arc_eachIterate[1])
                else:
                    neighbors_Temp.append(arc_eachIterate[1])
        return neighbors_Temp
                
    def getUnassignedNotCompletedVariables(self):
        return self.unassigned_variables

    def assignVariable_SetTheCell(self, variable, value):
        self.sudoku__.setTheActiveCell(variable, value)

    def checkTheConstraints(self):
        isSatisfied = True
        for perConstraint in self.constraintsRules:
            isSatisfied = isSatisfied and self.checkTheDifference(perConstraint)
        return isSatisfied

    def checkTheDifference(self, Checkthevariables__):
        lengthOftheVariable = len(Checkthevariables__)
        for idx in xrange(lengthOftheVariable - 1):
            if self.sudoku__.getCurrentCell(Checkthevariables__[idx]) != 0:
                for col in xrange(idx + 1, lengthOftheVariable):
                    if self.sudoku__.getCurrentCell(Checkthevariables__[col]) != 0:
                        if self.sudoku__.getCurrentCell(Checkthevariables__[idx]) == self.sudoku__.getCurrentCell(Checkthevariables__[col]):
                            return False
        return True

#
# # Test client
# # TODO: Fix maximum recursion, because the backtraacking search is not properly implemented, does not work on puzzle 4
if __name__ == "__main__":
    s = "000100702030950000001002003590000301020000070703000098800200100000085060605009000"
    sudoku = SudokuBoard(s)

    print "Sudoku Inicial:"
    print sudoku
    csp = SudokuBoardCSPAlgo(sudoku)
    AC3_Algo(csp)
    x = BackCheckS(csp)
    #print x
    for var in x:
        csp.customDomain[var] = [x[var]]
    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.customDomain[row + col][0])

    print "Sudoku Final:"
    print SudokuBoard(sol)

