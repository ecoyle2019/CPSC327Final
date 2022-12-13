from tile import Tile, HeightError

class Board:
    
    # ROWS = 5
    # COLUMNS = 5

    def __init__(self):
        # self.board = self.make_board()
        self.board = BoardBuilder().board


    # def make_board(self):
    #     '''Calls board builder to construct the product (the board made up of tiles)'''
    #     bb = BoardBuilder()   
    #     return bb

    def update_board(self):
        pass


# Board should use Memento pattern


class BoardBuilder:
    
    def __init__(self):
        self.tiles_built = 0
        self.rows_built = 0
        # self.worker_places = {'A': 16, 'B': 8, 'Y': 6, 'Z': 18} # starting places for workers--NOTE: this dict should be updated each time a worker moves
        self.board = self.build_board()

    # if tiles_built % 5 == 0 : start new row
    # if tiles_built in list(worker_places.values()) : tile.worker = {worker whose key corresponds to the value}

    # def get_worker(self):
    #     '''Returns which worker should be on a given tile'''
    #     for w in list(self.worker_places.items()):
    #         if self.tiles_built in w:
    #             return w[0]

    #     return None

    def create_tile(self):
        if self.tiles_built % 5 == 0 and self.tiles_built != 0:
            self.rows_built += 1
        
        t = Tile()

        t.row = self.rows_built # + 1
        t.column = self.tiles_built % 5
        return t

        # if t.column == 0:
        #     t.column = 5 # mod method works for all columns except the 5th, which will return 0, so this fixes that issue

        
        # if self.tiles_built in list(self.worker_places.values()):
        #     t.worker = self.get_worker() # updates worker positions on board, assuming self.worker_places is up to date

        

    def build_board(self):
        # IDEA: create an array for each row to get the entries for each row
        the_board = [ [], [], [], [], [] ]
        while self.tiles_built < 25:
            the_tile = self.create_tile()

            the_board[self.rows_built].append(the_tile)

            self.tiles_built += 1

        return the_board

# ROW = SELF.ROWS_BUILT
# COLUMN = SELF.TILES_BUILT % 5

# [ [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0] ]

if __name__ == "__main__":
    b = Board()


    
