import array
import math

import FastGrid
from ConvolutionKernel import ConvolutionKernel
from Grid_3 import Grid
from algorithms import prairie_fire, sigmoid


class UtilityCalculator:
    def compute_utility(self, grid: FastGrid) -> float:
        pass


class MaxTileCalculator:
    def compute_utility(self, grid: FastGrid) -> float:
        return grid.getMaxTile()


class FreeSpaceCalculator(UtilityCalculator):
    def __init__(self, weight=1.0):
        self.weight = weight

    def compute_utility(self, grid: FastGrid):
        return self.compute_utility_with_inverse(grid)

    def compute_utility_without_inverse(self, grid):
        space = len(grid.get_available_cells())
        return space * space

    def compute_utility_with_inverse(self, grid: FastGrid):
        space = len(grid.get_available_cells())
        space_ = (1.0 / space ** 0.9) if space > 0.0 else 1.0
        result = self.weight * min(1,
                                   1 - space_)  # this figure grows geometrically as space dwindles

        return result


class RoughnessCalculator(UtilityCalculator):
    def compute_utility(self, g: FastGrid):
        (less, more, eq) = (0, 1, 2)
        sign = None
        changed_signs = 0
        for y in range(3):
            for x in range(3):
                # first classify the sign of the two nums being considered
                if g[y, x] < g[y, x + 1]:
                    sign_new = less  # where False means we were on less
                elif g[y, x] == g[y, x + 1]:
                    sign_new = eq
                else:
                    sign_new = more
                # if this is the first comparison on the line then there is no chang score possible
                # so just record the sign and then move on
                if sign is None:
                    sign = sign_new
                    continue
                # if we get here then we are not on the first comparison so we can do additions
                if sign_new != eq and sign != sign_new:
                    changed_signs += 1
                sign = sign_new
        return changed_signs

        # def roughness_grid(self, grid, width, height):
        #     """Assumes something constructed like this:
        #     M = [[0,1,2], [3,4,5], [6,7,8]]
        #     that can be indexed like this M[0][2]"""
        #
        #     r = [[0.0] * width for _ in range(height)]
        #
        #     for y in range(0, height):
        #         for x in range(0, width):
        #             sum = 0.0
        #             cnt = 0.0
        #             rxlo = max(0, x - 1)
        #             rxhi = min(width - 1, x + 1)
        #             rylo = max(0, y - 1)
        #             ryhi = min(height - 1, y + 1)
        #             v = math.log(grid[x][y], 2) if grid[x][y] != 0.0 else 0.0
        #             for i in range(rylo, ryhi + 1):
        #                 for j in range(rxlo, rxhi + 1):
        #                     if i != y or j != x:
        #                         n1 = math.log(grid[i][j], 2) if grid[i][j] != 0.0 else 0.0
        #                         sum += abs(v - n1)
        #                         cnt += 1.0
        #             r[x][y] = sum / cnt if cnt > 0.0 else 0.0
        #     return r
        #
        # def roughness(self, grid, width, height):
        #     sum = 0.0
        #     r = self.roughness_grid(grid, width, height)
        #     for y in range(0, height):
        #         for x in range(0, width):
        #             sum += r[x][y]
        #     return sum / (width * height)


class MonotonicityCalculator(UtilityCalculator):
    """
calculate the monotonicity of a grid


Original Performance (100000 calls using UtilityCalculatorTests.test_profile_monotonicity_calculator
             16433615 function calls in 9.892 seconds

       Ordered by: internal time

       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       100000    3.115    0.000    9.892    0.000 UtilityCalculation.py:51(compute_utility)
      4533510    2.160    0.000    3.245    0.000 UtilityCalculation.py:55(get)
      2400000    1.190    0.000    1.190    0.000 Grid_3.py:172(crossBound)
      2400000    1.176    0.000    2.366    0.000 Grid_3.py:175(getCellValue)
      2400000    1.109    0.000    3.475    0.000 UtilityCalculation.py:52(not_zero)
      4400103    1.084    0.000    1.084    0.000 {built-in method math.log}
       200000    0.058    0.000    0.058    0.000 {built-in method builtins.max}
            1    0.000    0.000    0.000    0.000 ABTestingBase.py:20(stop_profiling)
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

This needs to be no more than 0.09 s i.e. a 100 fold improvement is required to get the depth needed

    """

    def compute_utility(self, grid: FastGrid):
        a = grid.board
        totals = array.array('i', [0, 0, 0, 0])

        # // up/down direction
        for x in range(4):
            current = 0
            neighbour = current + 1
            while neighbour < 4:
                while neighbour < 4 and a[(neighbour * 4) + x] == 0:
                    neighbour += 1
                if neighbour >= 4:
                    neighbour -= 1
                current_value = a[(current * 4) + x]  # get_val(a, x, current)
                next_value = a[(neighbour * 4) + x]  # get_val(a, x, neighbour)
                if current_value < next_value:
                    totals[0] += next_value - current_value
                elif next_value < current_value:
                    totals[1] += current_value - next_value
                current = neighbour
                neighbour += 1
                #
        # // left/right direction
        for y in range(4):
            current = 0
            neighbour = current + 1
            while neighbour < 4:
                while neighbour < 4 and a[(y * 4) + neighbour] == 0:
                    neighbour += 1
                if neighbour >= 4:
                    neighbour -= 1
                current_value = a[(y * 4) + current]  # get_val(a, current, y)
                next_value = a[(y * 4) + neighbour]  # get_val(a, neighbour, y)
                if current_value < next_value:
                    totals[2] += next_value - current_value
                elif next_value < current_value:
                    totals[3] += current_value - next_value
                current = neighbour
                neighbour += 1
        result = max(totals[0], totals[1]) + max(totals[2], totals[3])
        return sigmoid(result)

    def compute_utility_original(self, grid: FastGrid):
        def not_zero(g: Grid, x, y):
            return g.getCellValue((x, y)) != 0.0

        def get(g: Grid, a, b):
            v = g.map[a][b]
            return math.log(v, 2) if v != 0.0 else 0.0

        totals = [0, 0, 0, 0]

        # // up/down direction
        for x in range(4):
            current = 0
            neighbour = current + 1
            while neighbour < 4:
                while neighbour < 4 and not not_zero(grid, x, neighbour):
                    neighbour += 1
                if neighbour >= 4:
                    neighbour -= 1
                current_value = get(grid, x, current)
                nextValue = get(grid, x, neighbour)
                if current_value > nextValue:
                    totals[0] += nextValue - current_value
                elif nextValue > current_value:
                    totals[1] += current_value - nextValue
                current = neighbour
                neighbour += 1
                #
        # // left/right direction
        for y in range(4):
            current = 0
            neighbour = current + 1
            while neighbour < 4:
                while neighbour < 4 and not not_zero(grid, neighbour, y):
                    neighbour += 1
                if neighbour >= 4:
                    neighbour -= 1
                current_value = get(grid, current, y)
                nextValue = get(grid, neighbour, y)
                if current_value > nextValue:
                    totals[2] += nextValue - current_value
                elif nextValue > current_value:
                    totals[3] += current_value - nextValue
                current = neighbour
                neighbour += 1
        return max(totals[0], totals[1]) + max(totals[2], totals[3])


class ClusteringCalculator(UtilityCalculator):
    # https://raw.githubusercontent.com/datumbox/Game-2048-AI-Solver/master/src/com/datumbox/opensource/ai/AIsolver.java

    def compute_utility(self, g: FastGrid) -> float:
        clusteringScore = 0
        neighbors = [-1, 0, 1]
        for i in range(g.size):
            for j in range(g.size):
                v = g[i, j]
                if v == 0:
                    continue
                clusteringScore -= v
                numOfNeighbors = 0
                acc = 0
                for k in neighbors:
                    x = i + k
                    if x < 0 or x >= g.size:
                        continue
                    for l in neighbors:
                        y = j + l
                        if y < 0 or y >= g.size:
                            continue
                        if g[x, y] > 0:
                            numOfNeighbors += 1
                            acc += abs(v - g[x, y])
                clusteringScore += acc / numOfNeighbors
        return clusteringScore


class Kernel2(UtilityCalculator):
    """See https://codemyroad.wordpress.com/2014/05/14/2048-ai-the-intelligent-bot/"""

    def __init__(self):
        self.weight = array.array('f', [0.135759, 0.121925, 0.102812, 0.099937,
                                        0.0997992, 0.0888405, 0.076711, 0.0724143,
                                        0.060654, 0.0562579, 0.037116, 0.0161889,
                                        0.0125498, 0.00992495, 0.00575871, 0.00335193])

    def compute_utility(self, grid: FastGrid) -> float:
        scores = [0.0] * 8

        def fn(x, y):
            return self.weight[(y * 4) + x]

        for r in range(4):
            for c in range(4):
                scores[0] += grid[r, c] * fn(r, c)
                scores[1] += grid[r, c] * fn(3 - c, r)
                scores[2] += grid[r, c] * fn(3 - r, 3 - c)
                scores[3] += grid[r, c] * fn(c, 3 - r)

                scores[4] += grid[r, c] * fn(c, r)
                scores[5] += grid[r, c] * fn(r, 3 - c)
                scores[6] += grid[r, c] * fn(3 - c, 3 - r)
                scores[7] += grid[r, c] * fn(3 - r, c)
        return sigmoid(max(scores))


class MisplacedMaxTilePenalty(UtilityCalculator):
    def compute_utility(self, b: FastGrid) -> float:
        m = b.getMaxTile()
        return -1 * math.pow((b[0, 0] != m) * abs(b[0, 0] - m), 2)


class FastSnakeCalculator(UtilityCalculator):
    def compute_utility(self, g: FastGrid) -> float:
        b = g.board[0:4] + array.array('i', reversed(g.board[4:8])) + g.board[8:12] + array.array('i', reversed(
            g.board[12:16]))
        result = sum(x / 10 ** n for n, x in enumerate(b))
        return sigmoid(result)


class ClusterAnalysisCalculator(UtilityCalculator):
    def __init__(self):
        self.rewards_for_top_score = {
            0: 0,
            2: 0,
            4: 0,
            8: 0,
            16: 0,
            32: 0,
            64: 0,
            128: 0,
            256: 10,
            512: 20,
            1024: 50,
            2048: 100,  # job done.. .  .
            4096: 200,
            8192: 400,
            16384: 800,
            32768: 800,
            65536: 800
        }
        self.rewards_for_cluster_sizes = {
            0: 0,
            2: 1,
            4: 2,
            8: 3,
            16: 4,
            32: 5,
            64: 6,
            128: 7,
            256: 8,
            512: 9,
            1024: 10,
            2048: 11,
            4096: 12,
            8192: 13,
            16384: 14,
            32768: 15,
            65536: 16
        }
        self.penalties_for_cluster_fragments = {
            0: 0,
            2: 15,
            4: 14,
            8: 13,
            16: 12,
            32: 11,
            64: 10,
            128: 9,
            256: 8,
            512: 7,
            1024: 6,
            2048: 5,
            4096: 4,
            8192: 3,
            16384: 2,
            32768: 1,
            65536: 0
        }
        self.rewards_for_cluster_dimensions_x = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        self.rewards_for_cluster_dimensions_y = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

    def compute_utility(self, grid: FastGrid) -> float:
        r = prairie_fire(grid)
        rewards = 0.0
        penalties = 0.0
        top_score_reward = 0
        for tile in r:
            clusters = r[tile]
            num_clusters = len(clusters)
            if num_clusters > 0:
                top_score_reward = self.rewards_for_top_score[tile]
                max_cluster_size = max(c['count'] for c in clusters)
                penalties += 3.0**num_clusters
                rewards += 1.5**max_cluster_size
            #
            #
            # for cluster in clusters:
            #     # {'count': 0, 'minx': 1000, 'maxx': -1, 'miny': 5, 'maxy': -1, 'adjacent_tiles': []}
            #
            #
            #
            #     rewards += (self.rewards_for_cluster_sizes[tile] * cluster['count']) #if cluster['count'] >= 2 else 0
            #     rewards += self.rewards_for_cluster_dimensions_x[cluster['maxx'] - cluster['minx']]
            #     rewards += self.rewards_for_cluster_dimensions_y[cluster['maxy'] - cluster['miny']]
            # special_reward_for_zeros = sum(x['count'] for x in r[0])
            # rewards += 10 * special_reward_for_zeros
            rewards += top_score_reward
        return sigmoid(rewards - penalties)


class ConvolutionKernelCalculator(UtilityCalculator):
    def __init__(self):
        self.hole_detector_kernel = ConvolutionKernel([[-1, -1, -1],
                                                       [-1, +8, -1],
                                                       [-1, -1, -1]])


    def compute_utility(self, grid: FastGrid) -> float:
        new_array = self.hole_detector_kernel.compute(grid)
        result = sigmoid(sum(new_array))
        return result
