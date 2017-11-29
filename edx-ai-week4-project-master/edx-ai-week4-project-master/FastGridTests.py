from array import array

from ABTestingBase import ABTestingBase
from FastGrid import *
from Util import Util


class FastGridTests(ABTestingBase):
    def test_can_create_1(self):
        x = FastGrid()
        self.assertIsNotNone(x)

    def test_gives_acceptable_moves(self):
        sut = self.create_grid_from(array('i', [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0]))
        self.assertEqual(sut[2, 1], 2, 'should have been a 2 at this position')
        self.assertEqual(sut[3, 1], 2, 'should have been a 2 at this position')
        # acceptable moves are UP, DOWN, LEFT, RIGHT
        moves = sut.moves
        self.assertEqual(4, len(moves), 'can move in every direction')

    def test_gives_acceptable_moves_2(self):
        sut = self.create_grid_from(array('i', [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]))
        # acceptable moves are UP, DOWN, RIGHT
        moves = sut.moves
        self.assertEqual(3, len(moves), 'can move in every direction')
        self.assertFalse(sut.canMoveWith(LEFT_VEC))

    def test_gives_acceptable_moves_3(self):
        sut = self.create_grid_from(array('i', [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]))
        # acceptable moves are UP, DOWN, LEFT
        moves = sut.moves
        self.assertEqual([UP, DOWN, LEFT], moves, 'can move in every direction')
        self.assertFalse(sut.canMoveWith(RIGHT_VEC))

    def test_move_up_should_be_ok(self):
        sut = self.create_grid_from(array('i', [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]))
        # acceptable moves are UP, DOWN, LEFT
        self.assertTrue(sut.canMoveWith(UP_VEC))
        success, g2 = sut.move(UP)
        self.assertIsNotNone(g2)
        self.assertTrue(success)

    def test_move_down_should_be_ok(self):
        sut = self.create_grid_from(array('i', [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0]))
        # acceptable moves are UP, DOWN, LEFT
        self.assertTrue(sut.canMoveWith(DOWN_VEC))
        success, g2 = sut.move(DOWN)
        self.assertIsNotNone(g2)
        self.assertTrue(success)




