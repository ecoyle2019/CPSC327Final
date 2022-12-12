import sys

# from Santorini import *
from board import Board
# command line defaults (in order, from argv[1] to argv[4]): white_player=human, blue_player=human, enable_un_re=off, enable_score_display=off

#NOTE: these are only here bc I can't call them from Santorini until everything is working
class NotAValidWorkerError(Exception):
    """Given Worker was not a valid worker"""
    pass 

class NotValidDirectionError(Exception):
    """Given direction was not a valid direction"""
    pass

class AttemptedToMoveIntoBlockedTileError(Exception):
    """Can't move into tile at max height"""
    pass

class AttemptedToMoveIntoOccupiedTileError(Exception):
    """Can't move into tile at max height"""
    pass

class OutOfBoundsError(Exception):
    """Worker tried to move out of boundary of board"""
    pass



class SantoriniCLI:
    '''Command line interface for Santorini game'''


    def __init__(self, white_player='human', blue_player='human', enable_un_re='off', enable_score_display='off'): # see how to reflect values found in command line args

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

        self.turn_number = 1

        self.run_game()

        # NOTE: may need to assert command line args are valid (ex. white_player in ['human', 'heuristic', 'random'])

        # self.current_player = self.get_player()
        
    def run_game(self):
        
        while not self.is_won():
            self.display_prompt()

            # do stuff

            self.turn_number += 1

    def print_board(self):
        '''Used to format and print board to stdout.'''
        row_divider = "+--+--+--+--+--+"
        board = Board().board
        # print(board)

        print(row_divider)

        for row in board:
            for t in row:
                print(f"|{t.height} ", end='')
                # add check for worker—-if no worker on tile, add space
            print(f"|\n{row_divider}")


    # TODO: change so this function returns true when the game is won
    def is_won(self):
        return False

    def get_player(self):
        if self.turn_number % 2 == 1:
            return "white (AB)"
        else:
            return "blue (YZ)"

    def get_score_display(self):
        # TODO: figure out how scoring works -- idrk
        print(", FIGURE OUT SCORING")
        pass

    def display_prompt(self):

        self.print_board()
        print(f"Turn: {self.turn_number}, {self.get_player()}", end='')

        if self.enable_score_display == 'on':
            self.get_score_display()
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
        while not the_worker:
            try:
                the_worker = input("Select a worker to move\n")
                # do stuff w the_worker
            except NotAValidWorkerError:
                print("Not a valid direction")

        move_direction = None
        while not move_direction:
            try:
                move_direction = input("Select a direction to move\n")
                # do stuff with move_direction
            except NotValidDirectionError:
                print("Not a valid direction")
            except (AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError):
                print(f"Cannot move {move_direction}")


        build_direction = None
        while not build_direction:
            try:
                build_direction = input("Select a direction to build\n")
                # do stuff with build_direction
            except NotValidDirectionError:
                print("Not a valid direction")
            except (AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError):
                print(f"Cannot build {move_direction}")



if __name__ == "__main__":
    # setup sql database (if we use) + anything else

    game = SantoriniCLI()

    # game.print_board()
    print(sys.argv[1])
    