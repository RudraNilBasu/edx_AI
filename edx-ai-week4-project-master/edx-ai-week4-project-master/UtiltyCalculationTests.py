from array import array

import Util
from ABTestingBase import ABTestingBase
from UtilityCalculation import RoughnessCalculator, MonotonicityCalculator, FreeSpaceCalculator
from CompositeCalculation import CompositeUtilityCalculator
from KernelCalculator import KernelCalculator


class UtilityCalculationTests(ABTestingBase):
    def test_mono3_func(self):
        gstart = self.create_grid_from(array('i', [256, 32, 128, 2, 4, 16, 16, 64, 32, 4, 2, 2, 4, 0, 4, 4]))
        gdown = self.create_grid_from(array('i', [256, 0, 128, 2, 4, 32, 16, 64, 32, 16, 2, 2, 4, 4, 4, 4]))
        p = MonotonicityCalculator()
        ustart = p.compute_utility(gstart)
        udown = p.compute_utility(gdown)
        self.assertGreater(ustart, udown)

    def test_profile_composite_calculator(self):
        limit = 100000
        gs = [self.create_random_fastgrid() for _ in range(limit)]
        self.start_profiling()
        sut = CompositeUtilityCalculator()
        for g in gs:
            x = sut.compute_utility(g)
        self.stop_profiling()
        self.display_profiling_summary()

    def test_profile_monotonicity_calculator(self):
        limit = 100000
        gs = [self.create_random_fastgrid() for _ in range(limit)]
        self.start_profiling()
        sut = MonotonicityCalculator()
        for g in gs:
            x = sut.compute_utility(g)
        self.stop_profiling()
        self.display_profiling_summary()

    def test_profile_roughness_calculator(self):
        limit = 100000
        gs = [self.create_random_fastgrid() for _ in range(limit)]
        self.start_profiling()
        sut = RoughnessCalculator()
        for g in gs:
            x = sut.compute_utility(g)
        self.stop_profiling()
        self.display_profiling_summary()

    def test_profile_free_space_calculator(self):
        limit = 100000
        gs = [self.create_random_fastgrid() for _ in range(limit)]
        self.start_profiling()
        sut = FreeSpaceCalculator()
        for g in gs:
            x = sut.compute_utility(g)
        self.stop_profiling()
        self.display_profiling_summary()

    def test_profile_grid_to_array(self):
        limit = 100000
        gs = [self.create_random_fastgrid() for _ in range(limit)]
        sut = Util.Util.grid_to_array
        self.start_profiling()
        for g in gs:
            x = sut(g.map)
        self.stop_profiling()
        self.display_profiling_summary()

    def test_profile_grid_to_list(self):
        limit = 100000
        gs = [self.create_random_fastgrid() for _ in range(limit)]
        sut = Util.Util.grid_to_list
        self.start_profiling()
        for g in gs:
            x = sut(g.map)
        self.stop_profiling()
        self.display_profiling_summary()

    def test_snake_score_delivers_expected_result(self):
        sut = KernelCalculator()
        better = self.get_snake_score(sut, [256, 32, 128, 2,
                                            4,   16, 16,  64,
                                            32,  4,  2,   2,
                                            0,   0,  0,   0])
        worse = self.get_snake_score(sut, [2, 0, 0, 0, 256, 32, 128, 2, 4, 16, 16, 64, 32, 4, 2, 2])
        self.assertGreater(better, worse)

    def test_snake_score_delivers_expected_result_2(self):
        sut = KernelCalculator()
        better = self.get_snake_score(sut, [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        worse = self.get_snake_score(sut, [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertGreater(better, worse)

    def test_snake_score_delivers_expected_result_3(self):
        sut = KernelCalculator()
        better = self.get_snake_score(sut, [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        worse = self.get_snake_score(sut, [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertGreater(better, worse)

    def test_snake_score_delivers_expected_result_4(self):
        sut = KernelCalculator()
        better = self.get_snake_score(sut, [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        worse = self.get_snake_score(sut, [0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertGreater(better, worse)

    def test_snake_score_delivers_expected_result_5(self):
        sut = KernelCalculator()
        better = self.get_snake_score(sut, [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        worse = self.get_snake_score(sut, [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0])
        self.assertGreater(better, worse)

    def test_snake_score_delivers_expected_result_6(self):
        sut = KernelCalculator()
        start = self.get_snake_score(sut, [32, 4, 0, 0,
                                           4, 4, 0, 0,
                                           0, 4, 0, 0,
                                           2, 0, 0, 0])
        end = self.get_snake_score(sut, [32, 4, 0, 0,
                                         8, 0, 0, 0,
                                         4, 0, 0, 0,
                                         2, 0, 0, 0])
        preferred = self.get_snake_score(sut, [32, 4, 0, 0,
                                           4, 8, 0, 0,
                                           2, 0, 0, 0,
                                           0, 0, 0, 0])
        self.assertGreater(preferred, end)

    def test_get_large_scofre(self):
        sut = KernelCalculator()
        better = self.get_snake_score(sut, [4096, 1024, 512, 32, 64, 128, 256, 16, 8, 4, 2, 0, 0, 0, 0, 0])
        print(better)

    def get_snake_score(self, sut, l):
        g = self.create_grid_from(array('i', l))
        return sut.compute_utility(g)
