class ChessBoard:
    def __init__(self, squares = []):
        self.squares = squares
        self.lastPieceMoved = None
        self.consideringEnPassant = False

class Square():
    def __init__(self, isWhite = None, isOccupied = False, x = None, y = None, piece = None):
        self.isWhite = isWhite
        self.isOccupied = isOccupied
        self.x = x
        self.y = y
        self.piece = piece
        self.image_path = None
        self.image = None

        if isWhite:
            self.image_path = "../img/white.png"
        else:
            self.image_path = "../img/black.png"