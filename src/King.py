class King:
    def __init__(self, x = None, y = None, path = None, square = None, isWhite = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 90
        self.width = 96
        self.isWhite = isWhite

    def validate(self, newX, newY, board):
        VALID_DIFFERENCES = [[1,1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]
        difference = [newX - self.x, newY - self.y]

        # If invalid movement, return False
        if difference not in VALID_DIFFERENCES:
            return False

        # If valid movement and square is not occupied, return True
        # If square is occupied, return True if different colour (capture), else return False
        # Some simplification using De Morgan's Laws leads to the following expression
        return not board.squares[newX][newY].isOccupied or (self.isWhite != board.squares[newX][newY].piece.isWhite)