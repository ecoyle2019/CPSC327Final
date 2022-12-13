#Worker class


NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'
NORTHEAST = 'ne'
NORTHWEST = 'nw'
SOUTHEAST = 'se'
SOUTHWEST = 'sw'

MIN_BOUND = 0
MAX_BOUND = 4

class OutOfBoundsError(Exception):
    """Worker tried to move out of boundary of board"""
    pass

class NotValidDirectionError(Exception):
    """Given direct was not a valid direction"""

class Worker():
    """Worker Class with name and position given in row/col format"""
    #Should we pass in reference to board? Player?
    
    def __init__(self, name, row=0, col=0):
        """Creates a Worker with a name"""
        self.name = name
        self.row = row
        self.col = col
    
    def move_to(self, row, col):
        if(row < MIN_BOUND or row > MAX_BOUND or col < MIN_BOUND or col > MAX_BOUND):
            raise OutOfBoundsError()
        self.row = row
        self.col = col

    def move_direction(self, dir):
        """Move to a """
        if(dir == NORTH):
            self.move_to(self.row, self.col - 1)
        elif(dir == SOUTH):
            self.move_to(self.row, self.col + 1)
        elif(dir == EAST):
            self.move_to(self.row + 1, self.col)
        elif(dir == WEST):
            self.move_to(self.row - 1, self.col)
        elif(dir == NORTHEAST):
            self.move_to(self.row + 1, self.col - 1)
        elif(dir == NORTHWEST):
            self.move_to(self.row - 1, self.col - 1)
        elif(dir == SOUTHEAST):
            self.move_to(self.row + 1, self.col + 1)
        elif(dir == SOUTHWEST):
            self.move_to(self.row - 1, self.col + 1)
        else:
            raise NotValidDirectionError


    
    #Will take in a Move class as input, have to first implement Move class
    #def move()

    #generate list of possible moves
    #def getPossibleMoves()

    #Saturday
    #Basically just moves right now, need to see if we should pass in board here to handles certain errors
    
