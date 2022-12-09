#Tile Class

class Tile():
    MAX_HEIGHT = 4
    def __init__(self):
        self.height = 0
        #self.worker = None
    
    def build(self):
        if (self.height >= 4):
            #raise error
        self.height = self.height + 1