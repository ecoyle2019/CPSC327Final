from Tile import *

from Worker import Worker
from board import Board
from Player import Player
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

class NotYourWorkerError(Exception):
    """Given Worker that did not belong to player"""
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
    def __init__(self, player_one, player_two):

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
        self.commandfuture = []

        self.turn = 0

    def perform_action(self):
        self.current_player = self.players[self.turn %2]
        while True:
            try:
                self.select_worker(self.current_player.select_worker())
                break
            except NotYourWorkerError:
                print("That is not your worker")
                pass
            except NotAValidWorkerError:
                print("Not a valid worker")
                pass
                

        while True:
            try:
                move_direction = self.current_player.select_move(self.currently_selected_worker)
                self.move(move_direction)
                break
            except NotValidDirectionError:
                print("Not a valid direction")
                pass
                
            except (AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError):
                print(f"Cannot move {move_direction}")
                pass
                

        while True:
            try:
                build_direction = self.current_player.select_build(self.currently_selected_worker)
                self.build(build_direction)
                break
            except NotValidDirectionError:
                print("Not a valid direction")
                pass
            except (AttemptedToMoveIntoBlockedTileError, AttemptedToMoveIntoOccupiedTileError, OutOfBoundsError):
                print(f"Cannot build {build_direction}")
                pass

        self.current_player.print_action(self.currently_selected_worker.name, move_direction, build_direction)
        self.turn+=1

    def select_worker(self, worker): 
        for p in self.current_player.pieces:
            if p.name == worker:
                self.currently_selected_worker = p
                return
        other_player = self.players[(self.turn + 1) %2]
        for p in other_player.pieces:
            if p.name == worker:
                raise NotYourWorkerError
        raise NotAValidWorkerError        

    def move(self, direction):

        new_row_col = self.check_valid_move(direction, move=True)
        move = MoveCommand(self.currently_selected_worker, new_row_col[0], new_row_col[1])
        move.execute()

        self.commandhistory.append(move)

    def build(self, direction):

        new_row_col = self.check_valid_move(direction)
        build = BuildCommand(self.board.board[new_row_col[0]][new_row_col[1]])
        
        build.execute()
        self.commandhistory.append(build)

    def check_valid_move(self, dir, move=False):
        old_r = self.currently_selected_worker.row
        old_c = self.currently_selected_worker.col
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
            #print(f"Row: {new_r}\n")
            #print(f"Col: {new_c}\n")
            raise OutOfBoundsError
        
        if self.board.board[new_r][new_c].height > self.board.board[old_r][old_c].height + 1:
            raise AttemptedToMoveIntoBlockedTileError

        # if self.board.board[new_r][new_c].height >= MAX_HEIGHT: #change to match board implementation
        #     raise AttemptedToMoveIntoBlockedTileError
        # ADDED STATE
        if self.board.board[new_r][new_c].state.name == 'Blocked':
            raise AttemptedToMoveIntoBlockedTileError
        
        # allworkers = self.players[0].pieces + self.players[1].pieces
        # for x in allworkers:
        #     if x.row == new_r and x.col == new_c:
        #         raise AttemptedToMoveIntoOccupiedTileError
        # ADDED STATE
        if self.board.board[new_r][new_c].state.name == 'Occupied':
            raise AttemptedToMoveIntoOccupiedTileError
        
        # if move:
        #     if self.board.board[new_r][new_c].height > self.board.board[old_r][old_c].height + 1:
        #         raise AttemptedToMoveIntoBlockedTileError

        # ADDED STATE -- old tile is no longer occupied; new tile is now occupied
        if move:
            self.board.board[old_r][old_c].toggle_state(is_occupied=False)

            # change new tile's state to Occupied unless the tile is in its Winning State
            if self.board.board[new_r][new_c].state.name != 'Winning':
                self.board.board[new_r][new_c].toggle_state(is_occupied=True)
        else:
            # if not move, it means we're building
            self.board.board[new_r][new_c].toggle_state(is_occupied=False)

        return [new_r, new_c]

    def print_board(self):
        '''Used to format and print board to stdout.'''
        row_divider = "+--+--+--+--+--+"
        board = self.board.board
        allworkers = self.players[0].pieces + self.players[1].pieces
        # print(board)
        self.current_player = self.players[self.turn % 2]

        print(row_divider)

        for row in board:
            for t in row:
                print(f"|{t.height}", end='')
                occupied = False
                for w in allworkers:
                    if w.row == t.row and w.col == t.column:
                        print(f"{w.name}", end='')
                        occupied = True
                        # t.toggle_state(is_occupied=True) # ADDED STATE -- don't put here
                        break
                if occupied == False:
                    # t.toggle_state(is_occupied=False) # ADDED STATE -- don't put here
                    print(f" ", end='')
                
            print(f"|\n{row_divider}")
        


    def get_possible_moves(self, worker):
        poss_rows = [worker.row - 1, worker.row, worker.row + 1]
        poss_cols = [worker.col - 1, worker.col, worker.col + 1]

        occupied_tiles = []
        for w in self.players[0].pieces:
            occupied_tiles.append((w.row, w.col))

        for b in self.players[1].pieces:
            occupied_tiles.append((b.row, b.col))


        temp_poss_moves = list(itertools.product(poss_rows, poss_cols))
        poss_moves = []
        #print(worker.name)
        for m in temp_poss_moves:
            # if m[0] > 4 or m[1] > 4:
            #     poss_moves.remove(m)

            # if m[0] < 0 or m[1] < 0:
            #     poss_moves.remove(m)
            if m[0] in range(5) and m[1] in range(5) and (m[0], m[1]) not in occupied_tiles and self.board.board[m[0]][m[1]].height <= self.board.board[worker.row][worker.col].height + 1 and self.board.board[m[0]][m[1]].height != 4:
                #print(m)
                poss_moves.append(m)

        return poss_moves


    def get_possible_builds(self, worker):
        poss_rows = [worker.row - 1, worker.row, worker.row + 1]
        poss_cols = [worker.col - 1, worker.col, worker.col + 1]

        occupied_tiles = []
        for w in self.players[0].pieces:
            occupied_tiles.append((w.row, w.col))

        for b in self.players[1].pieces:
            occupied_tiles.append((b.row, b.col))


        temp_poss_builds = list(itertools.product(poss_rows, poss_cols))
        poss_builds = []
        #print(worker.name)
        for m in temp_poss_builds:
            # if m[0] > 4 or m[1] > 4:
            #     poss_moves.remove(m)

            # if m[0] < 0 or m[1] < 0:
            #     poss_moves.remove(m)
            if m[0] in range(5) and m[1] in range(5) and (m[0], m[1]) not in occupied_tiles and self.board.board[m[0]][m[1]].height != 4:
                #print(m)
                poss_builds.append(m)
        #print(poss_builds)
        return poss_builds


    def get_possible_move_scores(self, worker, row, col):
        '''Given a possible move to tile (row, col), return the sub-scores for that move'''
        # one idea for this is to keep track of the original row and column, and try moving to each possible position by calling worker.move_direction for all possible directions
        # after the worker is temporarily moved, call methods to get the scores then after storing the results in an array, reset the worker position to the start, and return the array
        # NOTE: it should also calculate the score for the current position: if the current position of a worker has a higher score than any possible moves, don't move that worker
        orig_row = worker.row
        orig_col = worker.col

        current_player = self.current_player
        if current_player == self.players[0]:
            opponent_player = self.players[1]
        else:
            opponent_player = self.players[0]

        try:

            worker.move_to(row, col)
        except OutOfBoundsError:
            pass
            #print(row, col)

        sub_scores = [self.get_height_score(worker), self.get_center_score(worker), self.get_distance_score(current_player, opponent_player)]
        
        worker.move_to(orig_row, orig_col)
        
        return sub_scores


    def get_height_score(self, worker):
        
        row_idx = worker.row
        col_idx = worker.col
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

        worker1 = self.players[self.turn % 2].pieces[0]
        worker2 = self.players[self.turn % 2].pieces[1]

        # possible_moves = self.get_possible_moves()
        worker1_moves = self.get_possible_moves(worker1)
        worker2_moves = self.get_possible_moves(worker2)

        w1_scores = {}
        w2_scores = {}

        for w1 in worker1_moves:
            w1_scores[(w1[0], w1[1])] = self.get_possible_move_scores(worker1, w1[0], w1[1])

        for w2 in worker2_moves:
            w2_scores[(w2[0], w2[1])] = self.get_possible_move_scores(worker2, w2[0], w2[1])

        return [w1_scores, w2_scores]

    def redo(self):
        try:
            move_command = self.commandfuture.pop()
            build_command = self.commandfuture.pop()
            if(build_command != None and move_command != None):
                move_command.execute()
                build_command.execute()
                self.turn+=1
                self.commandhistory.append(move_command)
                self.commandhistory.append(build_command)
        except IndexError:
            pass

    def undo(self):
        try:
            build_command = self.commandhistory.pop()
            move_command = self.commandhistory.pop()
            if(build_command != None and move_command != None):
                build_command.unexecute()
                move_command.unexecute()
                self.turn-=1
                self.commandfuture.append(build_command)
                self.commandfuture.append(move_command)
        except IndexError: 
            pass

    def next(self):
        self.commandfuture = []
    

    def is_won(self):

        # checking if white won
        for w in self.players[0].pieces:
            if self.board.board[w.row][w.col].height == 3:
                print("white has won")
                return True

        sum_moves = 0
        for w in self.players[0].pieces:
            sum_moves += len(self.get_possible_moves(w))

                
        if sum_moves == 0:
            print("blue has won")
            return True
        # checking if blue won
        for b in self.players[1].pieces:
            if self.board.board[b.row][b.col].height == 3:
                print("blue has won")
                return True
        
        sum_moves = 0
        for b in self.players[1].pieces:
            sum_moves += len(self.get_possible_moves(b))
        
        
        if sum_moves == 0:
            print("white has won")
            return True

        return False
