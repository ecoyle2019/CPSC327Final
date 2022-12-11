from Tile import Tile
from Worker import Worker
from board import Board
from Player import Player, HeuristicPlayer, RandomPlayer
from Command import MoveCommand, BuildCommand


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
        

        s#elf.workers = []
        player_one.pieces = whiteworkers
        player_two.pieces = blueworkers 

        self.players = [player_one, player_two]

        self.currently_selected_worker = None
        self.current_player = None

        self.commandhistory = []

        self.turn = 0

    
    def select_worker(self, worker): 
        self.current_player = self.players[self.turn %2]
        names = [p.name for p in self.current_player.pieces]

        if worker in names:
            self.currently_selected_worker = self.current_player.pieces[0] #fix this
        else: 
            raise NotAValidWorkerError

    def move(self, direction):
        if self.check_valid_move(direction):
            move = MoveCommand(self.currently_selected_worker, direction)
        
        move.execute()

        self.commandhistory.append(move)

    def build(self, direction):
        row = 0
        col = 0
        if self.check_valid_move(direction):
            build = BuildCommand(board[row][col])
        
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

        if board[new_r][new_c].height >= MAX_HEIGHT: #change to match board implementation
            raise AttemptedToMoveIntoBlockedTileError
        
        allworkers = self.players[0].pieces + self.players[1].pieces
        for x in allworkers:
            if x.row == new_r and x.col == new_c:
                raise AttemptedToMoveIntoOccupiedTileError
        
        return True

        