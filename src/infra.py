class ChessBoard:
    def __init__(self, squares = []):
        self.squares = squares

class Square:
    def __init__(self, isWhite = None, isOccupied = None, x = None, y = None, piece = None):
        self.isWhite = isWhite
        self.isOccupied = isOccupied
        self.piece = isOccupied
        self.x = x
        self.y = y
        self.piece = piece
        self.image_path = None
        self.image = None

        if isWhite:
            self.image_path = "../img/white.png"
        else:
            self.image_path = "../img/black.png"