class Bishop:
    def __init__(self, x = None, y = None, path = None, square = None, isWhite = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 80
        self.width = 96
        self.isWhite = isWhite

    def validate(self, newX, newY, board):
        # If invalid movement return False
        if abs(newX - self.x) != abs(newY - self.y):
            return False

        add_to_x = 0 if self.x == newX else (1 if newX > self.x else -1)
        add_to_y = 0 if self.y == newY else (1 if newY > self.y else -1)

        # If any obstacles in the way, return False
        x, y = self.x + add_to_x, self.y + add_to_y
        for i in range(max(abs(newX - self.x), abs(newY - self.y)) - 1):
            if board.squares[x][y].isOccupied:
                return False
            x += add_to_x
            y += add_to_y

        # If destination is not occupied, return True.
        # If destination is occupied, but occupied by a different colour, return True. Else return False.
        return not board.squares[newX][newY].isOccupied or (self.isWhite != board.squares[newX][newY].piece.isWhite)
        
