import unittest

import math


def roughness_grid(grid, width, height):
    """Assumes something constructed like this:
    M = [[0,1,2], [3,4,5], [6,7,8]]
    that can be indexed like this M[0][2]"""

    r = [[0.0] * width for _ in range(height)]

    for y in range(0, height):
        for x in range(0, width):
            sum = 0.0
            cnt = 0.0
            rxlo = max(0, x - 1)
            rxhi = min(width-1, x + 1)
            rylo = max(0, y - 1)
            ryhi = min(height-1, y + 1)
            v = math.log(grid[x][y], 2) if grid[x][y] != 0.0 else 0.0

            for i in range(rylo, ryhi+1):
                for j in range(rxlo, rxhi+1):
                    if i != y or j != x:
                        n1 = math.log(grid[i][j], 2) if grid[i][j] != 0.0 else 0.0
                        sum += abs(v - n1)
                        cnt += 1.0
            r[x][y] = sum / cnt if cnt > 0.0 else 0.0
    return r

def roughness(grid, width, height):
    sum = 0.0
    r = roughness_grid(grid, width, height)
    for y in range(0, height):
        for x in range(0, width):
            sum += r[x][y]
    return sum / (width * height)

class SmoothnessTests(unittest.TestCase):
    def test_non_rough_grid_has_score_zero(self):
        m = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        actual = roughness(m, 3, 3)
        expected = 0.0
        self.assertEqual(expected, actual)

    def test_more_rough_grid_has_higher_score(self):
        m = [[2, 4, 2], [2, 4, 2], [2, 2, 8]]
        actual = roughness(m, 3, 3)
        expected = 0.0
        self.assertLess(expected, actual)

    def test_more_rough_grid_has_higher_score2(self):
        m1 = [[2, 4, 2], [2, 4, 2], [2, 2, 8]]
        m2 = [[2, 4, 2], [2, 4, 2], [2, 2, 512]]
        a1 = roughness(m1, 3, 3)
        a2 = roughness(m2, 3, 3)
        self.assertLess(a1, a2)
