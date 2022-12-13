import sys

from Santorini import Santorini, NotAValidWorkerError,  NotValidDirectionError, AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError
from board import Board
from Player import Player
# command line defaults (in order, from argv[1] to argv[4]): white_player=human, blue_player=human, enable_un_re=off, enable_score_display=off

#NOTE: these are only here bc I can't call them from Santorini until everything is working



class SantoriniCLI:
    '''Command line interface for Santorini game'''


    def __init__(self, white_player='human', blue_player='human', enable_un_re='off', enable_score_display='off'): # see how to reflect values found in command line args

        # each should be in a separate try-except block
        try:
            self.white_player = sys.argv[1]
            self.blue_player = sys.argv[2]
            self.enable_un_re = sys.argv[3]
            self.enable_score_display = sys.argv[4]
        except IndexError:
            self.white_player = white_player
            self.blue_player = blue_player
            self.enable_un_re = enable_un_re
            self.enable_score_display = enable_score_display

        self.game = Santorini(Player(self.white_player, "white"), Player(self.blue_player, "blue"))
        self.turn_number = 1

        
        #self.run_game()

        # NOTE: may need to assert command line args are valid (ex. white_player in ['human', 'heuristic', 'random'])

        # self.current_player = self.get_player()
        
    def run_game(self):
        
        while not self.is_won():
            self.display_prompt()
            self.turn_number += 1
            self.game.turn += 1

        return


    # TODO: change so this function returns true when the game is won
    def is_won(self):

        # checking if white won
        for w in self.game.players[0].pieces:
            if self.game.board.board[w.row][w.col].height == 3:
                print("white has won")
                return True

        # checking if blue won
        for b in self.game.players[1].pieces:
            if self.game.board.board[b.row][b.col].height == 3:
                print("blue has won")
                return True

        return False

    def get_player(self):
        if self.turn_number % 2 == 1:
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

        self.game.print_board()

        print(f"Turn: {self.turn_number}, {self.get_player()}", end='')

        if self.enable_score_display == 'on':
            print(f", {self.get_score_display()}")
        else:
            print("")

        if self.enable_un_re == 'on':
            action = input("undo, redo, next\n").lower()
            while action not in ['undo', 'redo', 'next']:
                action = input("undo, redo, next\n")

            
            if action == 'undo':
                # do stuff
                pass
            elif action == 'redo':
                # do stuff
                pass
            # if action == 'next': continue with the prompt

        the_worker = None
        while True:
            try:
                the_worker = input("Select a worker to move\n")
                # do stuff w the_worker
                self.game.select_worker(the_worker)
                break
            except NotAValidWorkerError:
                print("Not a valid worker")

        move_direction = None
        while True:
            try:
                move_direction = input("Select a direction to move\n")
                self.game.move(move_direction)
                break
                # do stuff with move_direction
            except NotValidDirectionError:
                print("Not a valid direction")
            except (AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError):
                print(f"Cannot move {move_direction}")


        build_direction = None
        while True:
            try:
                build_direction = input("Select a direction to build\n")
                self.game.build(build_direction)
                break
                # do stuff with build_direction
            except NotValidDirectionError:
                print("Not a valid direction")
            except (AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError):
                print(f"Cannot build {build_direction}")



if __name__ == "__main__":
    # setup sql database (if we use) + anything else

    game = SantoriniCLI()
    game.run_game()
    # game.print_board()

    
    
