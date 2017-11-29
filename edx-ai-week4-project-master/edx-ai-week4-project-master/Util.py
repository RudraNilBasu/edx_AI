import array

import itertools

import math

from Grid_3 import Grid

common_logs = {0: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8, 512: 9, 1024: 10, 2048: 11,
               4096: 12, 8192: 13, 16384: 14, 32768: 15, 65536: 16}
primes = array.array('i', [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
                           97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
                           193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
                           293, 307, 311])

directions = {0: 'Up', 1: 'Down', 2: 'Left', 3: 'Right'}

class Util:
    @staticmethod
    def compute_grid_hashcode(g):
        if g.hashcode is not None:
            return g.hashcode
        hashcode = 0
        i = 0
        a = Util.grid_to_array(g)
        la = len(a)
        while i < la:
            hashcode += a[i] * primes[i]
            i += 1
        g.hashcode = hashcode
        return hashcode


    @staticmethod
    def slowgrid_to_list(g: Grid):
        x = g.map
        return x[0] + x[1] + x[2] + x[3]

    @staticmethod
    def fastgrid_to_array(g):
        return array.array('i', g.board)  # consider just passing the underlying board???

    @staticmethod
    def slowgrid_to_array(g: Grid):
        return array.array('i', Util.slowgrid_to_list(g))

    @staticmethod
    def array_to_2dlist(a: array):
        return Util.list_to_2dlist(a.tolist())

    @staticmethod
    def list_to_2dlist(l):
        return [l[0:4], l[4:8], l[8:12], l[12:16]]

    @staticmethod
    def not_zero(g: array, x, y, width=4):
        idx = (y * width) + x
        return g[idx] != 0

    @staticmethod
    def get_val(g: array, x, y, width=4):
        idx = (y * width) + x
        return g[idx]

    @staticmethod
    def get_log(g, a, b):
        v = Util.get_val(g, a, b, 4)
        return common_logs[v]

    @staticmethod
    def compute_kernel(width=4, ramp_amplification: float = None, create_snake: bool = False) -> list:
        weight = ramp_amplification if ramp_amplification is not None else 1.0
        if create_snake:
            return [math.exp(x) for x in [10, 8, 7, 6.5, .5, .7, 1, 3, -.5, -1.5, -1.8, -2, -3.8, -3.7, -3.5, -3]]
            # return [10, 8, 7, 6.5, .5, .7, 1, 3, -.5, -1.5, -1.8, -2, -3.8, -3.7, -3.5, -3]
            # r = [weight * x for x in range(16, -16, -2)]
            # tmp = Util.list_to_2dlist(r)
            # tmp[1] = list(reversed(tmp[1]))
            # tmp[3] = list(reversed(tmp[3]))
            # return array.array('f', tmp[0]+tmp[1]+tmp[2]+tmp[3])

        else:
            r = [0.0] * (width * width)
            min_val = math.pow(2, weight)
            max_val = math.pow((2 * (width - 1)) + 2, weight)
            total_range = max_val - min_val
            for row in range(0, width):
                for col in range(0, width):
                    idx = (row * width) + col
                    r[idx] = math.pow(row + col + 2, weight) - (total_range / 2) - min_val
            return r


    @staticmethod
    def any(fn, xs):
        result = False
        for x in xs:
            result = result or fn(x)
        return result
