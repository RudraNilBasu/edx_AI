from ABTestingBase import ABTestingBase
from FastGrid import FastGrid
from algorithms import prairie_fire


class PrairieFireTests(ABTestingBase):
    def test_can_light_fire_on_monotonous_grid(self):
        B = self.create_smooth_grid()
        r = prairie_fire(B)
        self.assertIsNotNone(r)

    def test_can_light_fire_on_thread_of_values_grid(self):
        B = self.create_fastgrid_from([2, 2, 2, 0,
                                       0, 0, 2, 0,
                                       0, 0, 2, 2,
                                       0, 0, 0, 2])  # 7 connected 2s
        r = prairie_fire(B)
        self.assertIsNotNone(r)
        self.assertEqual(r[2][0]['count'], 7)
        self.assertEqual(r[2][0]['minx'], 0)
        self.assertEqual(r[2][0]['maxx'], 3)
        self.assertEqual(r[2][0]['miny'], 0)
        self.assertEqual(r[2][0]['maxy'], 3)

        self.assertEqual(r[0][0]['count'], 7)
        self.assertEqual(r[0][0]['minx'], 0)
        self.assertEqual(r[0][0]['maxx'], 2)
        self.assertEqual(r[0][0]['miny'], 1)
        self.assertEqual(r[0][0]['maxy'], 3)

        self.assertEqual(r[0][1]['count'], 2)
        self.assertEqual(r[0][1]['minx'], 3)
        self.assertEqual(r[0][1]['maxx'], 3)
        self.assertEqual(r[0][1]['miny'], 0)
        self.assertEqual(r[0][1]['maxy'], 1)

    def test_can_distinguish_between_two_clusters(self):
        B = self.create_fastgrid_from([2, 2, 2, 0,
                                       0, 0, 0, 0,
                                       0, 0, 2, 2,
                                       0, 0, 0, 2])  # 2 groups of connected 2s each size 3
        r = prairie_fire(B)
        self.assertIsNotNone(r)
        self.assertTrue(r[2][0]['count'] == 3)
        self.assertEqual(r[2][0]['minx'], 0)
        self.assertEqual(r[2][0]['maxx'], 2)
        self.assertEqual(r[2][0]['miny'], 0)
        self.assertEqual(r[2][0]['maxy'], 0)

        self.assertTrue(r[2][1]['count'] == 3)
        self.assertEqual(r[2][1]['minx'], 2)
        self.assertEqual(r[2][1]['maxx'], 3)
        self.assertEqual(r[2][1]['miny'], 2)
        self.assertEqual(r[2][1]['maxy'], 3)

    def test_can_distinguish_between_two_cut_off_clusters(self):
        B = self.create_fastgrid_from([2, 2, 2, 0,
                                       64, 64, 64, 64,
                                       0, 0, 2, 2,
                                       0, 0, 0, 2])  # 2 groups of connected 2s each size 3
        r = prairie_fire(B)
        self.assertIsNotNone(r)
        self.assertTrue(r[2][0]['count'] == 3)
        self.assertTrue(r[2][1]['count'] == 3)
