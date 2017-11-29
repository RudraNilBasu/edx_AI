import sys

from ABTestingBase import ABTestingBase
from CaptureOutput import CaptureOutput
from Displayer_3 import Displayer
from GameBuilder import GameBuilder
from LogDisplayer import LogDisplayer, CompositeDisplayer


class GameplayTests(ABTestingBase):
    def test_profile_game(self):
        sut = GameBuilder().with_displayer(CompositeDisplayer()).build()
        self.start_profiling()
        sut.start()
        self.stop_profiling()
        self.display_profiling_summary('tottime')
        self.display_profiling_summary('ncalls')

    def test_can_run_game(self):
        sut = GameBuilder().with_displayer(Displayer()).build()
        sut.start()

    def test_optimise_player_weights(self):
        results = []
        runs = 1
        for max_tile_weight in range(0, 50, 2):
            for roughness_weight in range(0, -50, -2):
                for free_space_weight in range(1, 10, 2):
                    for monotonicity_weight in range(1, 50, 2):
                        acc = 0.0
                        max_score = -1 * sys.maxsize
                        min_score = sys.maxsize
                        sol = [free_space_weight, monotonicity_weight, roughness_weight, max_tile_weight]
                        print("testing:\t%s"%(str(sol)))
                        for i in range(1, 1+runs):
                            score = self.run_solution(sol)
                            acc += score
                            max_score = max(max_score, score)
                            min_score = min(min_score, score)
                            print("%d:\t%f"%(i, score))
                        avg_score = acc/runs
                        outcome = (avg_score, sol, max_score, min_score)
                        results.append(outcome)
                        self.display_result(outcome)
        sorted_results = sorted(results, lambda x: x[0])
        self.display_results(sorted_results)

    def run_solution(self, solution: list) -> int:
        self.suppress_output()
        sut = GameBuilder().build()
        sut.playerAI.set_weights(solution[0], solution[1], solution[2], solution[3])
        sut.start()
        self.allow_output()
        return sut.grid.getMaxTile()

    def display_results(self, rs:list):
        for r in rs:
            self.display_result(r)

    def display_result(self, r):
        print("%f:\t%s"%(r[0], r[1]))

