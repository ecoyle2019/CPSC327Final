from Worker import Worker


class Command():
    def execute():
        """Execute a command"""
        pass
    def unexecute():
        """Undo a command"""
        pass

class MoveCommand(Command):
    """Command to move a worker"""
    #so we need to decide if we're initializing with direction or position
    #def __init__(self, worker, direction):
    def __init__(self, worker, row, col):
        self.worker = worker
        #self.direction = direction
        self.new_row = row
        self.new_col = col
        self.prev_row = self.worker.row
        self.prev_col = self.worker.col

    def execute(self):
        
        #self.prev_row = self.worker.row
        #self.prev_col = self.worker.col
        self.worker.move_to(self.new_row, self.new_col)
    
    def unexecute(self):
        self.worker.move_to(self.prev_row, self.prev_col)

class BuildCommand(Command): 
    def __init__(self, tile):
        self.tile = tile
    def execute(self):
        self.tile.build()
    def unexecute(self):
        self.tile.unbuild()
    
