class Tile:

    MAX_HEIGHT = 4

    def __init__(self):
        self.height = '0'
        self.row = None # this is added upon creation
        self.column = None # added upon creation
        self.worker = None


    # attributes:
        # level built
        # worker occupying the space

    # methods:
        # 


# maybe use Factory pattern to create the tiles -- not sure
# State pattern for whether the tile is occupied and/or has an L4 building
    # state will be marked as free if there is no worker on it and no L4 building