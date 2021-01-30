class Pawn:
    def __init__(self, x = None, y = None, path = None, square = None, isWhite = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = 75
        self.width = 96
        self.isWhite = isWhite

    def validate(self, newX, newY, board):
        print(newX)
        print(newY)
        print(self.x)
        print(self.y)
        if not self.isWhite:
            if self.y == newY and (self.x + 1) == newX and not board.squares[newX][newY].isOccupied:
                return True
            if (self.y - 1) == newY and (self.x + 1) == newX and board.squares[newX][newY].isOccupied and board.squares[newX][newY].piece.isWhite:
                return True
            if (self.y + 1) == newY and (self.x + 1) == newX and board.squares[newX][newY].isOccupied and board.squares[newX][newY].piece.isWhite:
                return True
            if self.x == 1 and newX == 3 and self.y == newY and not board.squares[newX][newY].isOccupied and not board.squares[newX - 1][newY].isOccupied:
                return True

            return False

        if self.isWhite:
            print("Here, 26")
            print(board.squares[newX][newY].isOccupied)
            if self.y == newY and (self.x - 1) == newX and not board.squares[newX][newY].isOccupied:
                return True
            if (self.y - 1) == newY and (self.x - 1) == newX and board.squares[newX][newY].isOccupied and not board.squares[newX][newY].piece.isWhite:
                return True
            if (self.y + 1) == newY and (self.x - 1) == newX and board.squares[newX][newY].isOccupied and not board.squares[newX][newY].piece.isWhite:
                return True
            if self.x == 6 and newX == 4 and self.y == newY and not board.squares[newX][newY].isOccupied and not board.squares[newX + 1][newY].isOccupied:
                return True
            
            return False