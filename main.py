import sys
import random
from Strategy import *

from Santorini import Santorini
from board import Board
from Player import *
# command line defaults (in order, from argv[1] to argv[4]): white_player=human, blue_player=human, enable_un_re=off, enable_score_display=off

#NOTE: these are only here bc I can't call them from Santorini until everything is working



class SantoriniCLI:
    '''Command line interface for Santorini game'''


    def __init__(self, white_player_strategy='human', blue_player_strategy='human', enable_un_re=False, enable_score_display=True): # see how to reflect values found in command line args

        # each should be in a separate try-except block
        

        # self.game = Santorini(Player(self.white_player, "white"), Player(self.blue_player, "blue"))

        # if self.white_player == 'random':
        #     self.game.player_one = RandomPlayer("white")
        # elif self.white_player == 'heuristic':
        #     self.game.player_one = HeuristicPlayer("white")
        
        # if self.blue_player == 'random':
        #     self.game.player_two = RandomPlayer("blue")
        # elif self.blue_player == 'heuristic':
        #     self.game.player_two = HeuristicPlayer("blue")

        self.enable_un_re = enable_un_re
        self.enable_score_display = enable_score_display
        self.game = Santorini(Player("white", white_player_strategy), Player("blue", blue_player_strategy))
        Strategy.game = self.game

        
        #self.run_game()

        # NOTE: may need to assert command line args are valid (ex. white_player in ['human', 'heuristic', 'random'])

        # self.current_player = self.get_player()
        
    def run_game(self):
        
        while True:
            self.display_prompt()
            if(self.game.is_won()):
                break
            self.game.perform_action()

        # ADDED
        return # want to display board and turn after game is won -- will check if 


    # TODO: change so this function returns true when the game is won
   

    def get_player(self):
        if self.game.turn % 2 == 0:
            return "white (AB)"
        else:
            return "blue (YZ)"

    def get_score_display(self):
        # TODO: figure out how scoring works -- idrk
        # print(", FIGURE OUT SCORING")
        # score = self.game.score

        current_player = self.game.players[self.game.turn % 2]
        # opponent_player = self.game.players[(self.game.turn % 2) + 1]
        if current_player == self.game.players[0]:
            opponent_player = self.game.players[1]
        else:
            opponent_player = self.game.players[0]

        current_pieces = current_player.pieces
        height_score = 0
        center_score = 0
        distance_score = self.game.get_distance_score(current_player, opponent_player)

        for p in current_pieces:
            height_score += self.game.get_height_score(p)
            center_score += self.game.get_center_score(p)

        scores = [height_score, center_score, distance_score]

        return f"({scores[0]}, {scores[1]}, {scores[2]})"

    def display_prompt(self):

        if self.enable_un_re == True:
            while True:
                self.game.print_board()

                print(f"Turn: {self.game.turn + 1}, {self.get_player()}", end='')

                if self.enable_score_display == True:
                    print(f", {self.get_score_display()}")
                else:
                    print("")
                action = input("undo, redo, or next\n").lower()
                while action not in ['undo', 'redo', 'next']:
                    action = input("undo, redo, or next\n")


                if action == 'undo':
                    # do stuff
                    self.game.undo()
                    pass
                elif action == 'redo':
                    # do stuff
                    self.game.redo()
                # if action == 'next': continue with the prompt
                elif action == 'next':
                    self.game.next()
                    break
        else:
            self.game.print_board()

            print(f"Turn: {self.game.turn + 1}, {self.get_player()}", end='')

            if self.enable_score_display == True:
                print(f", {self.get_score_display()}")
            else:
                print("")




if __name__ == "__main__":
    # setup sql database (if we use) + anything else
    try:
        white_player_strategy = sys.argv[1]
    except IndexError:
        white_player_strategy = "human"

    try:
        blue_player_strategy = sys.argv[2]
    except IndexError:
        blue_player_strategy = "human"

    try:
        if sys.argv[3] == 'on':
            enable_un_re = True
        else:
            enable_un_re = False
    except IndexError:
        enable_un_re = False

    try:
        if sys.argv[4] == 'on':
            enable_score_display = True
        else:
            enable_score_display = False
    except IndexError:
        enable_score_display = False

    game = SantoriniCLI(white_player_strategy, blue_player_strategy, enable_un_re, enable_score_display)
    game.run_game()
    # game.print_board()

    
    
