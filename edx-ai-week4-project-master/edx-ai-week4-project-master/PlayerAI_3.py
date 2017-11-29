import multiprocessing
import sys
import time
from logging.handlers import RotatingFileHandler

from BaseAI_3 import BaseAI
from CompositeCalculation import CompositeUtilityCalculator
from FastGrid import FastGrid
from algorithms import *

deadline_offset = 0.1  # mandated solution timeout for exercise is .1 secs
max_depth_allowed = 6  # how deep to search for solutions

# some constants for initialising alpha and beta values in minimax
plus_infinity = float(sys.maxsize)
minus_infinity = -1.0 * plus_infinity


def init_logging():
    global log
    log = logging.getLogger('PlayerAI')
    log.setLevel(logging.DEBUG)
    fh = RotatingFileHandler('am-2048.log', mode='a', maxBytes=10000000, backupCount=3)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)


init_logging()


class PlayerAI(BaseAI):
    def __init__(self):
        self.fitness = CompositeUtilityCalculator()

    def invoke_minimax(self, ctx, soln, result_queue):
        score = minimax_with_ab_pruning(ctx, soln)
        result_queue.put((soln.move, score))

    def getMove(self, slowgrid):
        log.info("get move")
        grid = FastGrid(slowgrid)
        ctx = SolutionContext(board=grid
                              , depth=0
                              , alpha=-float("inf")
                              , beta=float("inf")
                              , timeout=time.process_time() + 0.1
                              , previous_move=None
                              , fn_fitness=lambda c, s: self.fitness.compute_utility(s.board)*
                                                        pow(0.9, max_depth_allowed - c.depth + 1)
                              , fn_terminate=lambda c, s: ctx.depth == max_depth_allowed or s.board.canMove())
        result_queue = multiprocessing.Queue()
        args = []
        for m in grid.get_moves(True):
            args.append((ctx, Solution(move=m,
                                       board=ctx.board.move(m.direction),
                                       is_max=True), result_queue))
        jobs = [multiprocessing.Process(target=self.invoke_minimax, group=None, args=mc) for mc in args]
        for job in jobs: job.start()
        for job in jobs: job.join()
        results = [result_queue.get() for arg in args]
        result = max(results, key=lambda s: s[1])
        return result[0].direction

# some resources
# http://www.wikihow.com/Beat-2048#Step_by_Step_Strategy_Guide_sub
# http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
