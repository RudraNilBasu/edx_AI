from array import array

# take kernels in the form:
# [[a, b, c],
#  [d, e, f],
#  [g, h, i]]
# all elements are floats
# size must be 3x3
class ConvolutionKernel():
    def __init__(self, arr):
        if len(arr) != 3:
            raise ValueError("incorrectly sized kernel")
        for row in arr:
            if len(row) != 3:
                raise ValueError("incorrectly sized kernel")
        self._arr = arr

    def compute(self, g):
        r = array('f', [0.0] * 16)
        for y in range(4):
            for x in range(4):
                r[(y*4)+x] = self.compute_point(x, y, g)
        return r

    def compute_point(self, x, y, g):
        acc = 0.0
        for i in range(0, 3):  # the extra +1 is because the upper bound is not inclusive
            for j in range(0, 3):  # the extra +1 is because the upper bound is not inclusive
                v = self.img(x - 1 + i, y - 1 + j, g)
                w = self.krnl(i, j)  # no need to offset the kernel
                acc += (v * w)
        return acc

    def img(self, x, y, g):
        # check that we are not too far out of bounds
        if x < -1 or x > 4:
            raise ValueError("x too far out of bounds")
        if y < -1 or y > 4:  # I'm sorry
            raise ValueError("y too far out of bounds")

        # this ensures that off edge values are just copies of the nearest on-board neighbour
        if x < 0: x = 0
        if y < 0: y = 0
        if x > 3: x = 3
        if y > 3: y = 3

        return g[x, y]

    def krnl(self, x, y):
        # check that we are not too far out of bounds
        if x < 0 or x > 3:
            raise ValueError("x out of bounds")
        if y < 0 or y > 3:  # I'm sorry
            raise ValueError("y out of bounds")

        return self._arr[x][y]