import logging

from KernelCalculator import KernelCalculator
from UtilityCalculation import *

log = logging.getLogger('app' + __name__)


class CompositeUtilityCalculator(UtilityCalculator):
    def __init__(self):
        self.calculators = [
            (1.0, ClusterAnalysisCalculator()),
            (0.0, ConvolutionKernelCalculator()),
            (0.0, FreeSpaceCalculator()),
            (0.0, RoughnessCalculator()),
            (0.0, MonotonicityCalculator()),
            (0.0, MaxTileCalculator()),
            (0.0, Kernel2()),
            (0.0, KernelCalculator()),
            (0.0, ClusteringCalculator()),
            (0.0, MisplacedMaxTilePenalty()),
            (0.0, FastSnakeCalculator())
        ]
        log.debug("Composite Calculator.")

    def compute_utility(self, grid: FastGrid) -> float:
        r = 0.0
        for weight, calculator in self.calculators:
            if weight != 0.0:
                r += weight * calculator.compute_utility(grid)
        return r

