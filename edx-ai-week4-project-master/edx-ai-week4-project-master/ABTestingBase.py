import cProfile
import unittest
import random

import math

import sys
from array import array

from CaptureOutput import CaptureOutput
from FastGrid import FastGrid
from Grid_3 import Grid
from PlayerAI_3 import PlayerAI


class ABTestingBase(unittest.TestCase):
    def setup(self):
        self.profiler = None

    def start_profiling(self):
        self.profiler = cProfile.Profile()
        self.profiler.enable()

    def stop_profiling(self):
        self.profiler.disable()

    def display_profiling_summary(self, default_sort_order='ncalls'):
        # sort_col = "tottime"
        # sort_col = "ncalls"
        self.profiler.print_stats(sort=default_sort_order)

    def create_empty_fastgrid(self) -> FastGrid:
        return self.create_fastgrid(0)

    def create_smooth_grid(self) -> FastGrid:
        return self.create_fastgrid(2)

    def create_fastgrid(self, val) -> FastGrid:
        sut = FastGrid()
        sut.board = array('i', [val]*16)
        return sut

    def create_slowgrid_from(self, val) -> Grid:
        sut = Grid()
        for row in range(4):
            for col in range(4):
                sut.setCellValue((row, col), val[row][col])
        return sut

    def create_slowgrid_from_list(self, l, size=4) -> FastGrid:
        sut = Grid()
        sut.map = l
        sut.size = size
        return sut

    def create_fastgrid_from(self, newboard, size=4) -> FastGrid:
        sut = FastGrid()
        sut.board = array('i', newboard)
        sut.size = size
        return sut

    def create_anti_monotonic_grid(self) -> FastGrid:
        sut = FastGrid()
        s = 4
        for x in range(s):
            for y in range(s):
                v = pow(2, ((s - 1 - x) + (s - 1 - y)))
                sut[x, y] = v if v > 1 else 0
        return sut

    def create_monotonic_grid(self) -> FastGrid:
        sut = FastGrid()
        s = 4
        for x in range(s):
            for y in range(s):
                v = pow(2, (x + y))
                sut[x, y] = v if v > 1 else 0
        return sut

    def create_player(self) -> PlayerAI:
        return PlayerAI()

    def create_random_fastgrid(self) -> FastGrid:
        r = FastGrid()
        tiles = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

        for x in range(4):
            for y in range(4):
                r[x, y] = random.choice(tiles)
        return r

    def suppress_output(self):
        sys.stdout = CaptureOutput()

    def allow_output(self):
        sys.stdout = sys.__stdout__
