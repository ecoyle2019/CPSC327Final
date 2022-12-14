
import random
from Strategy import InputStrategy, RandomStrategy, HeuristicStrategy

class NotSupportedPlayerType(Exception):
    """Not a supported Player Type"""
    pass

class Player:
    def __init__(self, name, strategy, pieces=None):
        self.name = name
        #self.side = side
        self.pieces = pieces
        #self.type = "Human"
        if strategy == "random":
            self.strategy = RandomStrategy()
        elif strategy == "heuristic":
            self.strategy = HeuristicStrategy()
        elif strategy == "human":
            self.strategy = InputStrategy()
        else:
            raise NotSupportedPlayerType

    def select_worker(self):
        return self.strategy.select_worker(self.pieces)
    def select_move(self, worker):
        return self.strategy.select_move(worker)
    def select_build(self, worker):
        return self.strategy.select_build(worker)
    def print_action(self, worker, move_dir, build_dir):
        return self.strategy.print_action(worker, move_dir, build_dir)
