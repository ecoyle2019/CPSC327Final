#Worker class
import Move
import Tile

class Worker():
    """Worker Class, can move, """
    #Should we pass in reference to board? Player?
    def __init__(self, name, position):
        """Creates a Worker with a name"""
        self.name = name
        self.position = position
    
    #Will take in a Move class as input, have to first implement Move class
    #def move()

    #generate list of possible moves
    #def getPossibleMoves()

    #Increment Tile by 1 of height is less than 4
    #def build(Tile tile):
