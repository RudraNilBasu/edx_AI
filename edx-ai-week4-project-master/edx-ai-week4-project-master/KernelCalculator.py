import FastGrid
from Util import Util
from UtilityCalculation import UtilityCalculator


class KernelCalculator(UtilityCalculator):
    def __init__(self, create_snake=True, ramp_amplification=2.0):
        self.kernel = Util.compute_kernel(create_snake=create_snake, ramp_amplification=ramp_amplification)

    def compute_utility(self, grid: FastGrid):
        return sum(x * y for (x,y) in zip(self.kernel, grid.board))
