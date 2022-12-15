class HeightError(Exception):
    '''Ensures building height is not more than 4 or less than 0'''
    pass


class TileState:
    '''Base state for tiles'''
    def __init__(self, tile):
        self.tile = tile


class PlayingState(TileState):
    '''Tile is in PlayingState if the height < 3 and no worker occupies the tile'''
    def __init__(self, tile):
        super().__init__(tile)
        self.name = 'Playing'

    def toggle_state(self, is_occupied):
        '''PlayingState can only toggle to Winning state or OccupiedState'''

        if is_occupied:
            self.tile.state = self.tile.occupied_state
        elif self.tile.height == 3:
            self.tile.state = self.tile.winning_state


class OccupiedState(TileState):
    '''Tile is in OccupiedState if a worker is currently on the tile'''
    def __init__(self, tile):
        super().__init__(tile)
        self.name = 'Occupied'

    def toggle_state(self, is_occupied):
        '''OccupiedState can toggle to any state'''

        if not is_occupied:
            if self.tile.height == 3:
                self.tile.state = self.tile.winning_state
            if self.tile.height == 4:
                self.tile.state = self.tile.blocked_state
            elif self.tile.height < 3:
                self.tile.state = self.tile.playing_state

class WinningState(TileState):
    '''Tile is in WinningState if the height is 3 -- player can win by moving worker onto tile'''
    def __init__(self, tile):
        # self.tile = tile
        super().__init__(tile)
        self.name = 'Winning'

    def toggle_state(self, is_occupied):
        '''WinningState can only toggle to BlockedState -- game would end if occupied'''

        if self.tile.height == 4:
            self.tile.state = self.tile.blocked_state
        elif self.tile.height < 3:
            if(is_occupied):
                self.tile.state = self.tile.occupied_state
            else:
                self.tile.state = self.tile.playing_state


class BlockedState(TileState):
    '''Tile is in BlockedState if the height is 4 -- no workers can move onto the tile'''
    def __init__(self, tile):
        # self.tile = tile
        super().__init__(tile)
        self.name = 'Blocked'

    def toggle_state(self, is_occupied):
        '''Blocked tile has no possible future states'''
        if self.tile.height == 3:
            self.tile.state = self.tile.winning_state
        if self.tile.height < 3 and not is_occupied:
            self.tile.state = self.tile.playing_state
        elif self.tile.height < 3 and is_occupied: 
            self.tile.state = self.tile.occupied__state
        pass


class Tile:

    MAX_HEIGHT = 4

    def __init__(self):
        self.height = 0
        self.row = None # this is added upon creation
        self.column = None # added upon creation

        self.playing_state = PlayingState(self)
        self.occupied_state = OccupiedState(self)
        self.blocked_state = BlockedState(self)
        self.winning_state = WinningState(self)
        self.state = self.playing_state


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


    def toggle_state(self, is_occupied=False):
        '''Toggles to new state if necessary'''
        self.state.toggle_state(is_occupied)
        