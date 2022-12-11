
import random


class Player:
    def __init__(self, name, side=None, pieces=None):
        self.name = name
        self.side = side
        self.pieces = pieces
    def get_move(self):
        pass

class RandomPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.type = "Random"
    
    def get_move(self, possible_moves):
        return random.choice(possible_moves)


class HeuristicPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Heuristic"
    
    def get_move(self, possible_moves):
        return  self.find_best_move(possible_moves)
    
    def find_best_move(possible_moves):
        return possible_moves[0]