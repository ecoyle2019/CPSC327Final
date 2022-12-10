from tile import Tile

class Board:
    
    # ROWS = 5
    # COLUMNS = 5

    def __init__(self):
        self.board = BoardBuilder()


    



# attributes:
    # 25 tiles
    # 4 workers

# methods:
    # isWon() - returns true if game is over (if a worker moves on top of space w level 3)

# Board should use Memento pattern


class BoardBuilder:
    
    def __init__(self):
        self.tiles_built = 0
        self.rows_built = 0
        self.worker_places = {'A': 17, 'B': 9, 'Y': 7, 'Z': 19} # starting places for workers--NOTE: this dict should be updated each time a worker moves
        self.build_board()

    # if tiles_built % 5 == 0 : start new row
    # if tiles_built in list(worker_places.values()) : tile.worker = {worker whose key corresponds to the value}

    def get_worker(self):
        '''Returns which worker should be on a given tile'''
        for w in list(self.worker_places.items()):
            if self.tiles_built in w:
                return w[0]

        return None

    def create_tile(self):
        if self.tiles_built % 5 == 0 and self.tiles_built != 0:
            self.rows_built += 1
        
        t = Tile()
        t.row = self.rows_built + 1
        t.column = self.tiles_built % 5

        if t.column == 0:
            t.column = 5 # mod method works for all columns except the 5th, which will return 0, so this fixes that issue

        
        if self.tiles_built in list(self.worker_places.values()):
            t.worker = self.get_worker() # updates worker positions on board, assuming self.worker_places is up to date

        return t

    def build_board(self):
        # IDEA: create an array for each row to get the entries for each row
        the_board = [ [], [], [], [], [] ]
        while self.tiles_built < 25:
            the_tile = self.create_tile()

            try:
                entry = the_tile.height + the_tile.worker
            except TypeError:
                entry = the_tile.height

            the_board[self.rows_built].append(entry) # number of rows completed will always be one less than the current row number, so it works for indexing

            self.tiles_built += 1

        print(the_board)
        # return the_board


    def format_board(self):
        board_divider = "+--+--+--+--+--+"
        board = self.build_board()
        
        # for now, I just want to see what the 2D board array looks like, so I'm just printing before figuring out formatting (need to figure out how to add column dividers)
        # print(self.board)

        r1 = board[0]
        
        return r1
        
        # return(str(type(board)))
   

    # def __str__(self):
    #     # return self.format_board()
    #     return self.build_board

# ROW = SELF.ROWS_BUILT
# COLUMN = SELF.TILES_BUILT % 5



if __name__ == "__main__":
    b = Board()

    print(b.board)