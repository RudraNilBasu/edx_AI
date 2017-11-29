#########################################################
# Author: Diego Palma S.
#
# Apply implemented algorithm for all test cases in .txt
# files, and checks whether it solves the sudokus properly
# This is an auxiliary file for project 3 in the course
# Artificial Intelligence offered by Columbia University
# through edX
#########################################################

from SudokuBoard import *
import time

with open('sudokus_start.txt') as temp_file:
    sudokus_start = [line.rstrip('\r\n') for line in temp_file]

with open('sudokus_finish.txt') as temp_file:
    sudokus_finish = [line.rstrip('\r\n') for line in temp_file]

N = len(sudokus_start)
for k in xrange(N):
    sudoku = SudokuBoard(sudokus_start[k])
    csp = SudokuBoardCSPAlgo(sudoku)
    AC3_Algo(csp)
    x = BackCheckS(csp)
    for var in x:
        csp.customDomain[var] = [x[var]]
    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.customDomain[row + col][0])

    print (k + 1, sol == sudokus_finish[k])
    
    time.sleep(0.001)
    
