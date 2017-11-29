import cProfile

import CompositeCalculation
from KernelCalculator import KernelCalculator
from ABTestingBase import ABTestingBase
from CompositeCalculation import CompositeUtilityCalculator
from Grid_3 import Grid
from PlayerAI_3 import PlayerAI
from Util import Util
from UtilityCalculation import MonotonicityCalculator, RoughnessCalculator

directions = [UP, DOWN, LEFT, RIGHT] = range(4)


class Player3Tests(ABTestingBase):
    def test_can_create_player_a_i(self):
        sut = PlayerAI()
        self.assertIsNotNone(sut)

    def test_can_create_grid_to_design(self):
        sut = Grid()
        self.assertIsNotNone(sut)
        self.assertEqual(4, sut.size)
        sut.setCellValue((0, 0), 2)
        self.assertEqual(sut.getCellValue((0, 0)), 2)

    def test_can_compute_any_monotonicity_score(self):
        g = self.create_monotonic_grid()
        sut = MonotonicityCalculator()
        actual = sut.compute_utility(g)
        self.assertIsNotNone(actual)

    def test_inverted_grids_have_same_monotonicity(self):
        g1 = self.create_monotonic_grid()
        g2 = self.create_anti_monotonic_grid()
        sut = MonotonicityCalculator()
        a1 = sut.compute_utility(g1)
        a2 = sut.compute_utility(g2)
        self.assertEqual(a2, a1)

    def test_monotonic_grids_should_have_positive_score(self):
        g1 = self.create_monotonic_grid()
        sut = MonotonicityCalculator()
        a1 = sut.compute_utility(g1)
        self.assertLess(0, a1)

    def test_uniform_grid_should_have_perfect_score(self):
        g1 = self.create_smooth_grid()
        sut = RoughnessCalculator()
        a1 = sut.compute_utility(g1)
        self.assertEqual(a1, 0.0)

    def test_empty_grid_smoothness_is_zero(self):
        g1 = self.create_empty_fastgrid()
        sut = RoughnessCalculator()
        a1 = sut.compute_utility(g1)
        self.assertEqual(a1, 0)

    def test_kernel(self):
        sut = KernelCalculator()
        self.assertIsNotNone(sut)

    def test_against_dumb_move_1(self):
        """Take from a real gameplay scenarios where a fatal wrong move was made:
            Computer's turn:

              256      32     128      2

               4       16      16      64

               32      4       2       2

               4       0       4       4

            Player's Turn:DOWN  (should have been RIGHT)

              256      0      128      2

               4       32      16      64

               32      16      2       2

               4       4       4       4


            RIGHT: [
                [256, 32, 128, 2],
                [0,   4,  32,  64],
                [0,   32, 4,   4],
                [0,   0,  4,   8]
                ]
            """
        p = CompositeCalculation.CompositeUtilityCalculator()
        gstart = self.create_fastgrid_from([256, 32, 128, 2,
                                        4, 16, 16, 64,
                                        32, 4, 2, 2,
                                        4, 0, 4, 4])
        gDOWN = self.create_fastgrid_from([256, 0, 128, 2,
                                       4, 32, 16, 64,
                                       32, 16, 2, 2,
                                       4, 4, 4, 4])
        ustart = p.compute_utility(gstart)
        udown = p.compute_utility(gDOWN)
        self.assertGreater(ustart, udown)
        gright = gstart.clone()
        gright.move(RIGHT)
        uright = p.compute_utility(gright)
        self.assertGreater(uright, udown)
        available_moves = gstart.moves
        self.assertNotEquals(1, len(available_moves))
        p1 = PlayerAI()
        suggestedMove = p1.getMove(gstart.to_slowgrid())
        self.assertNotEquals(suggestedMove, DOWN)

    def test_against_dumb_move_2(self):
        """Take from a real gameplay scenarios where a fatal wrong move was made:

starting position:

  128      32      8       4
   32      2      128      16
   0       2       8       8
   0       4       4       8

position after going down (which should not be the preferred choice)

   0       0       8       0
   0       32     128      4
  128      4       8       16
   32      4       4       16

                                """
        p = PlayerAI()
        g1 = self.create_slowgrid_from_list([[128, 32, 8, 4],
                                             [32, 2, 128, 16],
                                             [0, 2, 8, 8],
                                             [0, 4, 4, 8]])
        m = p.getMove(g1)
        self.assertNotEqual(m, DOWN, 'should not have chosen move Down')
        # PROBLEM:
        # Why does this test pass in a unit test, but when the game is being played the right move is not chosen?
        # KNOWN:
        #  - the choice could be influenced by a cache.
        #
        #
        #
        #
        #
        #


    def test_against_dumb_move_3(self):
        """Take from a real gameplay scenarios where a fatal wrong move was made:

Computer's turn:

   32  16  32 2
   4   16  4  2
   4   2   8  2
   2   4   8  2

Player's Turn:DOWN (should have been UP)

   0   0   0   0
   32  32  32  0
   8   2   4   4
   2   4   16  4

UP would have been:
   32  32  32  4
   8   2   4   4
   2   4   16  0
   0   0   0   0
                                """
        p = PlayerAI()
        gstart = self.create_fastgrid_from([32, 16, 32, 2,
                                        4, 16, 4, 2,
                                        4, 2, 8, 2,
                                        2, 4, 8, 2])
        ok, gdown = gstart.move(DOWN)
        ok, gup = gstart.move(UP)
        ce = CompositeUtilityCalculator()
        ustart = ce.compute_utility(gstart)
        udown = ce.compute_utility(gdown)
        uup = ce.compute_utility(gup)
        self.assertGreater(ustart, udown)
        self.assertGreater(uup, udown, "the UP move should have a higher score than the DOWN move")
        available_moves = gstart.moves
        self.assertNotEquals(1, len(available_moves), "there are two options (UP or DOWN)")
        chosen_move = p.getMove(gstart.to_slowgrid())
        self.assertNotEquals(chosen_move, DOWN, "down is the inferior move, and should not have been chosen")
        # clue: when run at full speed it chooses DOWN, but when slowed down it picks UP

    def test_weights_kernel_is_symetrical(self):
        sut = KernelCalculator(create_snake=False)
        self.assertAlmostEqual(sut.kernel[0] + sut.kernel[15], 0.0, 4)

    def test_can_compute_score(self):
        g1 = self.create_smooth_grid()
        sut = RoughnessCalculator()
        a1 = sut.compute_utility(g1)
        self.assertEqual(a1, 0.0)
