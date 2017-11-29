# a file to simply implement some key algorithms in a procedural fashion
from collections import namedtuple

import logging

import math


class SolutionContext:
    def __init__(self
                 , board=None
                 , alpha=None
                 , beta=None
                 , depth=None
                 , timeout=None
                 , previous_move=None
                 , fn_fitness=None
                 , fn_terminate=None):
        self.beta = beta
        self.alpha = alpha
        self.previous_move = previous_move
        self.board = board
        self.depth = depth
        self.timeout = timeout
        self.fn_fitness = fn_fitness
        self.fn_terminate = fn_terminate


class Solution:
    def __init__(self
                 , move=None
                 , board=None
                 , is_max=None):
        self.board = board
        self.is_max = is_max
        self.move = move


MinMove = namedtuple('MinMove', ['is_max', 'x', 'y', 'tile', 'prob'])
MaxMove = namedtuple('MaxMove', ['is_max', 'direction'])

def minimax(context: SolutionContext, solution: Solution):
    log = logging.getLogger('PlayerAI')
    log.info("minimax")
    if context.fn_terminate(context, solution):
        return context.fn_fitness(context, solution)
    moves = solution.board.get_moves(not solution.is_max)

    if solution.is_max:
        results = []
        for m in moves:
            new_context, new_solution = create_call_vars(m, context, solution)
            results.append(minimax(context=new_context,
                                   solution=new_solution))
        return max(results)
    else:
        results = []
        for m in moves:
            new_context, new_solution = create_call_vars(m, context, solution)
            r = minimax(context=new_context, solution=new_solution)
            r2 = r * new_solution.move.prob
            results.append(r2)
        return min(results)

def minimax_with_ab_pruning(context: SolutionContext, solution: Solution):
    log = logging.getLogger('PlayerAI')

    if context.fn_terminate(context, solution):
        return context.fn_fitness(context, solution)

    moves = solution.board.get_moves(solution.is_max)

    if solution.is_max:
        best_result = -float("inf")
        for m in moves:
            new_context, new_solution = create_call_vars(m, context, solution)
            result = minimax_with_ab_pruning(context=new_context, solution=new_solution)
            best_result = max(result, best_result)
            context.alpha = max(best_result, context.alpha)
            if context.alpha <= context.beta:
                log.debug("alpha cut")
                break
        return best_result
    else:
        # PROBLEM:
        #  - MIN is not playing to minimise the eventual score of MAX, it is generating tiles at random
        #    The result from MIN should be the average score achieved given the move by MAX.
        #    So, how is beta calculated to allow the alpha-beta pruning algorithm to be implemented?
        # KNOWN:
        #  - MIN should return the average across all possible moves
        #  - MAX can maximise the alpha based on that
        #  - MIN will be called on across several possible moves by MAX
        # IDEA:
        #  - Just set beta to the average?
        #

        best_result = float("inf")
        for m in moves:
            new_context, new_solution = create_call_vars(m, context, solution)
            result = minimax_with_ab_pruning(context=new_context, solution=new_solution)
            best_result = min(result, best_result)
            context.beta = min(best_result, context.beta)
            if context.alpha <= context.beta:
                log.debug("beta cut")
                break
        return best_result

        # acc = 0.0
        # for m in moves:
        #     new_context, new_solution = create_call_vars(m, context, solution)
        #     r = minimax_with_ab_pruning(context=new_context, solution=new_solution)
        #     acc += r * new_solution.move.prob
        # avg_score = acc / (len(moves) / 2)
        # context.beta = min(context.beta, avg_score)
        # return avg_score


def create_call_vars(move, context, solution):
    new_context = SolutionContext(board=solution.board,
                                  depth=context.depth + 1,
                                  timeout=context.timeout,
                                  previous_move=move,
                                  fn_fitness=context.fn_fitness,
                                  fn_terminate=context.fn_terminate)
    new_solution = Solution(move=move,
                            board=new_context.board.move(move),
                            is_max=not solution.is_max)
    return new_context, new_solution

def prairie_fire(g):
    def set_fire_to(B, x, y, t, code):
        # if off edge
        if x < 0 or x > 3 or y < 0 or y > 3:
            return False
        # if done already
        if B[x, y] == code:
            return False
        # if no match
        if B[x, y] != t:
            return False

        B[x, y] = code
        set_fire_to(B, x - 1, y, t, code)
        set_fire_to(B, x + 1, y, t, code)
        set_fire_to(B, x, y - 1, t, code)
        set_fire_to(B, x, y + 1, t, code)
        return True

    B = g.clone()
    result = dict()
    tiles = [2 ** l if l > 0 else 0 for l in range(0, 17)]
    for t in tiles:
        result[t] = []
    for t in tiles:
        code = -1
        for x in range(0, 4):
            for y in range(0, 4):
                lit = set_fire_to(B, x, y, t, code)
                if lit:
                    code -= 1
        # now gather the stats
        for c in range(-1, code - 1, -1):
            stats = {'count': 0, 'minx':1000, 'maxx': -1, 'miny':5, 'maxy': -1, 'adjacent_tiles': []}
            for x in range(0, 4):
                for y in range(0, 4):
                    if B[x,y] == c:
                        stats['count'] += 1
                        stats['minx'] = min(stats['minx'], x)
                        stats['maxx'] = max(stats['maxx'], x)
                        stats['miny'] = min(stats['miny'], y)
                        stats['maxy'] = max(stats['maxy'], y)
                        B[x,y] = 0
            if stats['count'] > 0:
                result[t].append(stats)
    return result



def sigmoid(x):
    return 1 / (1 + math.exp(-x))