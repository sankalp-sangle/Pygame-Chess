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
        self.jumpedTwoSquares = False

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
                self.jumpedTwoSquares = True
                return True
            # En Passant rule
            if self.x == 4 and newX == 5 and isinstance(board.lastPieceMoved, Pawn) and board.lastPieceMoved.jumpedTwoSquares and newY == board.lastPieceMoved.y and board.lastPieceMoved.x == 4:
                board.consideringEnPassant = True
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
                self.jumpedTwoSquares = True
                return True
            # En Passant rule
            if self.x == 3 and newX == 2 and isinstance(board.lastPieceMoved, Pawn) and board.lastPieceMoved.jumpedTwoSquares and newY == board.lastPieceMoved.y and board.lastPieceMoved.x == 3:
                board.consideringEnPassant = True
                return True
            
            return False