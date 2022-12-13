from Tile import Tile
from Worker import Worker
from board import Board
from Player import Player, HeuristicPlayer, RandomPlayer
from Command import MoveCommand, BuildCommand

import itertools

NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'
NORTHEAST = 'ne'
NORTHWEST = 'nw'
SOUTHEAST = 'se'
SOUTHWEST = 'sw'

MAX_HEIGHT = 4
MAX_BOUND = 4
MIN_BOUND = 0

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

class Santorini():
    def __init__(self, player_one, player_two, enable_undo=False, enable_score_display=False):
        self.enable_undo = enable_undo
        self.enable_score_display = enable_score_display

        self.board = Board()

        whiteworkers = [None] * 2
        blueworkers = [None] * 2

        blueworkers[0] = Worker("Y", 1, 1)
        blueworkers[1] = Worker("Z", 3, 3)

        whiteworkers[0] = Worker("A", 3, 1)
        whiteworkers[1] = Worker("B", 1, 3)
        

        #self.workers = []
        
        player_one.pieces = whiteworkers
        player_two.pieces = blueworkers 

        self.players = [player_one, player_two]

        self.currently_selected_worker = None
        self.current_player = None

        self.commandhistory = []

        self.turn = 0

    
    def select_worker(self, worker): 
        self.current_player = self.players[self.turn %2]

        for p in self.current_player.pieces:
            if p.name == worker:
                self.currently_selected_worker = p
                return

        raise NotAValidWorkerError        

    def move(self, direction):

        new_row_col = self.check_valid_move(direction)
        move = MoveCommand(self.currently_selected_worker, new_row_col[0], new_row_col[1])
        move.execute()

        self.commandhistory.append(move)

    def build(self, direction):

        new_row_col = self.check_valid_move(direction)
        build = BuildCommand(self.board.board[new_row_col[0]][new_row_col[1]])
        
        build.execute()
        self.commandhistory.append(build)

    def check_valid_move(self, dir):
        new_r = self.currently_selected_worker.row
        new_c = self.currently_selected_worker.col

        if(dir == NORTH):
            new_r -= 1
        elif(dir == SOUTH):
            new_r += 1
        elif(dir == EAST):
            new_c += 1
        elif(dir == WEST):
            new_c-= 1
        elif(dir == NORTHEAST):
            new_r -= 1
            new_c += 1
        elif(dir == NORTHWEST):
            new_r -= 1
            new_c -= 1
        elif(dir == SOUTHEAST):
            new_r += 1
            new_c += 1
        elif(dir == SOUTHWEST):
            new_r += 1
            new_c -= 1
        else:
            raise NotValidDirectionError

        if new_r > MAX_BOUND or new_c > MAX_BOUND or new_r < MIN_BOUND or new_c < MIN_BOUND:
            raise OutOfBoundsError

        if self.board.board[new_r][new_c].height >= MAX_HEIGHT: #change to match board implementation
            raise AttemptedToMoveIntoBlockedTileError
        
        allworkers = self.players[0].pieces + self.players[1].pieces
        for x in allworkers:
            if x.row == new_r and x.col == new_c:
                raise AttemptedToMoveIntoOccupiedTileError
        
        return [new_r, new_c]

    def print_board(self):
        '''Used to format and print board to stdout.'''
        row_divider = "+--+--+--+--+--+"
        board = self.board.board
        allworkers = self.players[0].pieces + self.players[1].pieces
        # print(board)

        print(row_divider)

        for row in board:
            for t in row:
                print(f"|{t.height}", end='')
                occupied = False
                for w in allworkers:
                    if w.row == t.row and w.col == t.column:
                        print(f"{w.name}", end='')
                        occupied = True
                        break
                if occupied == False:
                    print(f" ", end='')
                
            print(f"|\n{row_divider}")
        


    # call on self.currently_selected_worker
    def get_possible_moves(self, worker):
        poss_rows = [worker.row - 1, worker.row, worker.row + 1]
        poss_cols = [worker.col - 1, worker.col, worker.col + 1]


        poss_moves = list(itertools.product(poss_rows, poss_cols))

        for m in poss_moves:
            if m[0] > 5 or m[1] > 5:
                poss_moves.remove(m)

        return poss_moves


    def get_possible_move_scores(self, worker, row, col):
        '''Given a possible move to tile (row, col), return the sub-scores for that move'''
        # one idea for this is to keep track of the original row and column, and try moving to each possible position by calling worker.move_direction for all possible directions
        # after the worker is temporarily moved, call methods to get the scores then after storing the results in an array, reset the worker position to the start, and return the array
        # NOTE: it should also calculate the score for the current position: if the current position of a worker has a higher score than any possible moves, don't move that worker
        orig_row = worker.row
        orig_col = worker.col

        current_player = self.current_player
        # opponent_player = self.players[(self.turn % 2) + 1]
        if current_player == self.players[0]:
            opponent_player = self.players[1]
        else:
            opponent_player = self.players[0]

        worker.move_to(row, col)

        sub_scores = [self.get_height_score(worker), self.get_center_score(worker), self.get_distance_score(current_player, opponent_player)]
        
        worker.move_to(orig_row, orig_col)
        
        return sub_scores


    def get_height_score(self, worker):
        
        row_idx = worker.row - 1
        col_idx = worker.col - 1
        return self.board.board[row_idx][col_idx].height

    def get_center_score(self, worker):
        
        center_score = 0

        # iterate through the worker's possible moves (do separately for each worker)
        #NOTE: this implementation works if we (*temporarily*) move to each possible position to calculate score
                        
        # NOTE: row and column are indexed values (worker.row == 2 means third row of board)
        if worker.row == 2 and worker.col == 2:
            center_score += 2
        if (worker.row in [1, 3]) and (worker.col in [1, 2, 3]):
            center_score += 1
        if worker.row == 2 and worker.col in [1, 3]:
            center_score += 1
        if worker.row in [0, 4] or worker.col in [0, 4]:
            center_score += 0
        
        # print(worker.row, worker.col, center_score)
        return center_score


        
    # def get_score(self):
    #     '''Gets Heuristic score, which is used for Heuristic moves and score display'''

    #     current_player = self.current_player
    #     opponent_player = self.players[(self.turn % 2) + 1]


    def get_distance_score(self, current_player, opponent_player):

        # player_workers = [worker1, worker2]
        # opponent_workers = [worker1, worker2]
        player_workers = current_player.pieces
        opponent_workers = opponent_player.pieces

        worker1_d1 = max( abs(player_workers[0].row - opponent_workers[0].row), abs(player_workers[0].col - opponent_workers[0].col))
        worker1_d2 = max( abs(player_workers[0].row - opponent_workers[1].row), abs(player_workers[0].col - opponent_workers[1].col))

        worker2_d1 = max( abs(player_workers[1].row - opponent_workers[0].row), abs(player_workers[1].col - opponent_workers[0].col))
        worker2_d2 = max( abs(player_workers[1].row - opponent_workers[1].row), abs(player_workers[1].col - opponent_workers[1].col))

        d1 = min(worker1_d1, worker2_d1)
        d2 = min(worker1_d2, worker2_d2)
        distance_score = 8 - (d1 + d2)

        return distance_score


    def get_sub_scores(self):
        '''Returns the sub-scores for each possible move'''
        # go through each possible move and call self.get_possible_move_scores, and store in a dictionary -- return the dictionary (will be used in get_move_score())

        pass

