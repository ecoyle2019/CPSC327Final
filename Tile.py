class HeightError(Exception):
    '''Ensures building height is not more than 4 or less than 0'''
    pass


class Tile:

    MAX_HEIGHT = 4

    def __init__(self):
        self.height = 0
        self.row = None # this is added upon creation
        self.column = None # added upon creation
        self.worker = None


    # def __str__(self):
    #     ## print out height + worker (if it exists) -- also change self.height to an int, but convert to str in this method/

    

    # attributes:
        # level built
        # worker occupying the space

    # methods:
        # function that adds or substracts height (build and unbuild)

    def build(self):
        '''Updates height if it's legal to build'''
        if self.height < 4:
            self.height += 1
        else:
            raise HeightError("Cannot build above level 4")

    
    def unbuild(self):
        '''Updates height if it's legal to unbuild'''
        if self.height > 0:
            self.height -= 1
        else:
            raise HeightError("Building level cannot be negative")
        




# maybe use Factory pattern to create the tiles -- not sure
# State pattern for whether the tile is occupied and/or has an L4 building
    # state will be marked as free if there is no worker on it and no L4 building
