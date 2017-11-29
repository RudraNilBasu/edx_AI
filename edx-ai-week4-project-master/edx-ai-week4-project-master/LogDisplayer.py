import logging

from BaseDisplayer_3 import BaseDisplayer
from Displayer_3 import Displayer
from FastGrid import FastGrid

logging.basicConfig(
    filename="2048.log",
    format="%(levelname)-10s %(asctime)s %(message)s",
    level=logging.ERROR
)


class LogDisplayer:
    def __init__(self):
        self.log = logging.getLogger('app.moves')

    def display(self, grid):
        self.display_array_init(grid)

    def display_array_init(self, g):
        fg = FastGrid(g)
        self.log.info("%s" % str(fg.board))


class CompositeDisplayer(BaseDisplayer):
    def __init__(self):
        super().__init__()
        self.displayers = [Displayer(), LogDisplayer()]

    def display(self, grid):
        for displayer in self.displayers:
            displayer.display(grid)
