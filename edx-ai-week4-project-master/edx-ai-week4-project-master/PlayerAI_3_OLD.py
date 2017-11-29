import multiprocessing
import time

from BaseAI_3 import BaseAI
from CompositeCalculation import CompositeUtilityCalculator, AlgorithmWeights
from FastGrid import FastGrid
from Grid_3 import Grid
from PlayerAI_3 import log, deadline_offset, minus_infinity, plus_infinity, max_depth_allowed
from Util import directions


class PlayerAI_OLD(BaseAI):
    def __init__(self):
        self.deadline = None  # used to set a timeout on the exploration of possible moves
        self.moves = []
        # self.util_engine = KernelCalculator()
        self.util_engine = CompositeUtilityCalculator(AlgorithmWeights(free_space_weight=3.0
                                                                       , monotonicity_weight=1.0
                                                                       , roughness_weight=0.0
                                                                       , max_tile_weight=0.0
                                                                       , kernel_weight=0.0
                                                                       , clustering_weight=0.0))

    def set_weights(self, free_space_weight=0.0
                    , monotonicity_weight=0.0
                    , roughness_weight=0.0
                    , max_tile_weight=0.0
                    , kernel_weight=1.0
                    , clustering_weight=1.0):
        self.util_engine.weights = AlgorithmWeights(free_space_weight
                                                    , monotonicity_weight
                                                    , roughness_weight
                                                    , max_tile_weight
                                                    , kernel_weight
                                                    , clustering_weight)
        log.debug("weights", {
            'free_space_weight': free_space_weight
              , 'monotonicity_weight': monotonicity_weight
              , 'roughness_weight': roughness_weight
              , 'max_tile_weight': max_tile_weight
              , 'kernel_weight': kernel_weight
              , 'clustering_weight': clustering_weight})

    def getMove(self, slow_grid: Grid):
        log.debug("getting moves")
        grid = FastGrid(slow_grid)
        self.deadline = time.perf_counter() + deadline_offset

        result_queue = multiprocessing.Queue()
        args = []
        for m in grid.moves:
            s, g = grid.move(m)
            assert s, "moves must be valid"
            args.append((g, m, result_queue))
        jobs = [multiprocessing.Process(target=self.start_ab_search, group=None, args=mc) for mc in args]
        for job in jobs: job.start()
        for job in jobs: job.join()
        results = [result_queue.get() for mc in args]
        log.debug("results: %s",results)
        choice = max(results, key=lambda x: x[1])
        log.info("choice: %s, %0.3f", directions[choice[0]], choice[1])
        return choice[0]

    def start_ab_search(self, grid: FastGrid, move, result_queue):
        score = self.alphabeta_search((grid, move),
                                      minus_infinity,
                                      plus_infinity,
                                      True,
                                      max_depth_allowed)
        result_queue.put((move, score))

    def alphabeta_search(self, gm, alpha, beta, is_maximiser, depth, path=[]):
        (grid, _originating_move) = gm
        originating_move = _originating_move if _originating_move is not None else -1
        if depth == 0: #or time.perf_counter() >= self.deadline:
            score = self.util_engine.compute_utility(grid)
            log.debug("Leaf: %d %d %f", hash(grid), originating_move, score)
            return score

        if self.terminal_test(grid): #or time.perf_counter() >= self.deadline:
            score = self.util_engine.compute_utility(grid)
            log.debug("Terminal: %d %d %f", hash(grid), originating_move, score)
            return score

        # if time.perf_counter() >= self.deadline:
        #     score = self.util_engine.compute_utility(grid)
        #     log.debug("Timeout: %d %d %f", hash(grid), originating_move, score)
        #     return score

        if is_maximiser:
            result = minus_infinity

            for move in grid.moves:
                subpath = path+[('max', move)]
                ok, child_grid = grid.move(move)
                assert ok, "move should have been valid"
                s = self.alphabeta_search((child_grid, move),
                                          alpha,
                                          beta,
                                          False,
                                          depth - 1,
                                          subpath)
                # is this result better than anything I've seen on this node so far?
                result = max(result, s)
                # is this result better than anything I've seen on any node previously visited?
                alpha = max(alpha, result)

                # is this branch better than the worst that the minimiser can force me to?
                if beta <= alpha:
                    # if yes, then we can expect the minimiser to avoid this branch on principle.
                    log.debug("alpha cut: %s", subpath)
                    break
            return result
        else:
            result = plus_infinity
            sub_moves = self.getMinimizerMoves(grid)
            for minmove in sub_moves:
                subpath = path + [('min', minmove)]
                (child_grid, prob) = minmove
                s = self.alphabeta_search((child_grid, None),
                                          alpha,
                                          beta,
                                          True,
                                          depth - 1,
                                          subpath)
                result = min(result, s)
                beta = min(beta, result)
                if beta <= alpha:
                    log.debug("beta cut: %s", subpath)
                    break
            return result

    def terminal_test(self, grid: FastGrid):
        return not grid.canMove()

    def getMaximizerMoves(self, grid):
        moves = grid.get_available_moves()
        return moves

    def getMinimizerMoves(self, grid):
        # get the most likely cells
        cells = grid.get_available_cells()
        new_grids = []
        # possible_new_tiles = [2, 4]
        possible_new_tiles = [2, 4]
        for cell in cells:
            for new_value in possible_new_tiles:
                new_grid = grid.clone()
                new_grid.setCellValue(cell, new_value)
                new_grids.append((new_grid, 0.9 if new_value == 2 else 0.1))
        return new_grids


        # def utility6(self, grid: FastGrid):
        #     hash_key = self.compute_grid_hash_key(grid)
        #     ce = self.cache_grid_scores[hash_key]
        #     if ce is not None:
        #         ce._replace(hit_count=ce.hit_count + 1)
        #         self.cache_grid_scores[hash_key] = CacheEntry(str_repr=ce.str_repr, score=ce.score, hash_key=ce.hash_key,
        #                                                       hit_count=ce.hit_count + 1)
        #         return ce.score
        #     r = 0.0
        #
        #     if self.weights.max_tile_weight != 0.0:
        #         max_tile = grid.getMaxTile()
        #         r += max_tile * self.weights.max_tile_weight
        #     if self.weights.monotonicity_weight != 0.0:
        #         r += self.mono3(grid) * self.weights.monotonicity_weight
        #     if self.weights.roughness_weight != 0.0:
        #         r += self.roughness_fast(grid) * self.weights.roughness_weight
        #     if self.weights.free_space_weight != 0.0:
        #         space = len(grid.getAvailableCells())
        #         space_ = (1.0 / space ** 0.9) if space > 0.0 else 1.0
        #         crampedness = self.weights.free_space_weight * min(1,
        #                                                            1 - space_)  # this figure grows geometrically as space dwindles
        #         r *= crampedness  # cramped boards are to be avoided at all costs. Penalise them heavily
        #     ce = self.create_cache_entry(grid, r)
        #     self.cache_grid_scores[hash_key] = ce
        #     return r
        #
        # def utility5(self, grid: FastGrid):
        #     r = 0.0
        #     if self.weights.free_space_weight != 0.0:
        #         cells = len(grid.getAvailableCells())
        #         max_tile = grid.getMaxTile()
        #         r += cells * math.log(max_tile, 2) * self.weights.free_space_weight
        #     if self.weights.max_tile_weight != 0.0:
        #         max_tile = grid.getMaxTile()
        #         r += max_tile * self.weights.max_tile_weight
        #     if self.weights.monotonicity_weight != 0.0:
        #         r += self.dot_product(grid) * self.weights.monotonicity_weight
        #     if self.weights.roughness_weight != 0.0:
        #         r += self.clustering(grid) * self.weights.roughness_weight
        #     return r
        #
        # def utility4(self, grid: FastGrid):
        #     r = 0.0
        #     if self.weights.free_space_weight != 0.0:
        #         cells = len(grid.getAvailableCells())
        #         r += cells * self.weights.free_space_weight
        #     if self.weights.max_tile_weight != 0.0:
        #         max_tile = grid.getMaxTile()
        #         r += max_tile * self.weights.max_tile_weight
        #     if self.weights.monotonicity_weight != 0.0:
        #         r += self.dot_product(grid) * self.weights.monotonicity_weight
        #     if self.weights.roughness_weight != 0.0:
        #         r += self.roughness_fast(grid) * self.weights.roughness_weight
        #     return r

