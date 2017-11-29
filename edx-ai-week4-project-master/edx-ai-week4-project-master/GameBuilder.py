from BaseDisplayer_3 import BaseDisplayer
from ComputerAI_3 import ComputerAI
from GameManager_3 import GameManager
from Grid_3 import Grid
from PlayerAI_3 import PlayerAI


class GameBuilder:
    def __init__(self):
        self.grid = Grid()
        self.game_manager = GameManager()
        self.playerAI = PlayerAI()
        self.computerAI = ComputerAI()
        self.displayer = BaseDisplayer()

    def build(self) -> GameManager:
        self.game_manager.setDisplayer(self.displayer)
        self.game_manager.setPlayerAI(self.playerAI)
        self.game_manager.setComputerAI(self.computerAI)
        return self.game_manager

    def with_displayer(self, displayer: BaseDisplayer):
        self.displayer = displayer
        return self