import unittest

from Util import Util
from ABTestingBase import ABTestingBase
from Grid_3 import Grid
from Caching import GridCache


class GridCacheTests(ABTestingBase):
    def test_can_create_GridCache(self):
        sut = GridCache()
        self.assertIsNotNone(sut)

    def test_equal_grids_produce_equal_hash_codes(self):
        g1 = [[4, 0, 2, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        g2 = [[4, 0, 2, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        sut = GridCache()
        u1 = sut.compute_grid_hashcode(g1)
        u2 = sut.compute_grid_hashcode(g2)
        self.assertEqual(u1, u2, "equal grids should produce same hash code")

    def test_unequal_grids_produce_unequal_hash_codes(self):
        g1 = [[4, 0, 2, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        g2 = [[4, 0, 2, 4], [0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        sut = GridCache()
        u1 = sut.compute_grid_hashcode(g1)
        u2 = sut.compute_grid_hashcode(g2)
        self.assertNotEqual(u1, u2, "unequal grids should produce different hash code")

    def test_can_store_and_retrieve_different_values(self):
        g1 = self.create_grid(2)
        g2 = self.create_grid(4)
        sut = GridCache()
        sut[g1] = 5
        sut[g2] = 7
        self.assertIsNotNone(sut[g1])
        self.assertIsNotNone(sut[g2])
        self.assertEqual(sut[g1], 5)
        self.assertEqual(sut[g2], 7)

    def test_different_grids_have_distinct_values(self):
        g1 = self.create_grid(2)
        g2 = self.create_grid(4)
        sut1 = GridCache()
        sut2 = GridCache()
        sut1[g1] = 5
        sut2[g2] = 7
        self.assertIsNotNone(sut1[g1])
        self.assertIsNone(sut2[g1])
        self.assertIsNotNone(sut2[g2])
        self.assertIsNone(sut1[g2])
        self.assertEqual(sut1[g1], 5)
        self.assertEqual(sut2[g2], 7)

    def test_hash_duplicate_probably_doesnt_happen(self):
        limit = 10000
        sut = GridCache()
        while limit > 0:
            g1 = self.create_random_fastgrid()
            g2 = self.create_random_fastgrid()
            self.assertNotEqual(sut.compute_grid_hashcode(g1.map), sut.compute_grid_hashcode(g2.map))
            limit -= 1
    def test_cache_attach_hashcode_to_grid(self):
        g1 = self.create_random_fastgrid()
        hc1 = getattr(g1, 'hash_code', None)
        self.assertIsNone(hc1)
        hc_tmp = Util.compute_grid_hashcode(g1)
        self.assertIsNotNone(hc_tmp)
        hc2 = getattr(g1, 'hash_code', None)
        self.assertIsNotNone(hc2)
        self.assertEqual(hc_tmp, hc2)
