class Rook:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 78
        self.width = 96