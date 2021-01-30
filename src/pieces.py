class Pawn:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 75
        self.width = 96

class Rook:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 78
        self.width = 96

class Knight:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 75
        self.width = 96

class Bishop:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 80
        self.width = 96

class King:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 96
        self.width = 96

class Queen:
    def __init__(self, x = None, y = None, path = None, square = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 96
        self.width = 96