import sys
from SudokuBoard import *
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python driver.py <input_string> or python driver.py 003020600900305001001806400008102900700000008006708200002609500800203009005010300'
        sys.exit(0)
    sudokuBoard = SudokuBoard(sys.argv[1])
    cspAlgoritm = SudokuBoardCSPAlgo(sudokuBoard)
    AC3_Algo(cspAlgoritm)
    temp = BackCheckS(cspAlgoritm)
    for per in temp:
        cspAlgoritm.customDomain[per] = [temp[per]]

    solution = ""
    for row_vice in "ABCDEFGHI":
        for col_vice in "123456789":
            solution += str(cspAlgoritm.customDomain[row_vice + col_vice][0])

   # Enable the below line for debug
   # print 'the input is'
   # print sudokuBoard
   #  print 'the output is '
   #  print SudokuBoard(solution)
    with open("output.txt", "w") as output_result:
        output_result.write(solution)

