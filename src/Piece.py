class Piece:
    # Sprite size in pixels, used to center the image on its square. Overridden per piece.
    HEIGHT = 0
    WIDTH = 96

    def __init__(self, x = None, y = None, path = None, square = None, isWhite = None):
        self.x = x
        self.y = y
        self.image_path = path
        self.image = None
        self.square = square
        self.height = self.HEIGHT
        self.width = self.WIDTH
        self.isWhite = isWhite

    def validate(self, newX, newY, board):
        raise NotImplementedError

    def canLandOn(self, newX, newY, board):
        # A piece can land on an empty square or capture a piece of the other colour
        target = board.squares[newX][newY]
        return not target.isOccupied or target.piece.isWhite != self.isWhite


class SteppingPiece(Piece):
    # Pieces that jump straight to one of a fixed set of offsets (King, Knight)
    OFFSETS = ()

    def validate(self, newX, newY, board):
        if (newX - self.x, newY - self.y) not in self.OFFSETS:
            return False
        return self.canLandOn(newX, newY, board)


class SlidingPiece(Piece):
    # Pieces that slide any distance along a set of directions until blocked (Rook, Bishop, Queen)
    DIRECTIONS = ()

    def validate(self, newX, newY, board):
        dx, dy = newX - self.x, newY - self.y
        if dx == 0 and dy == 0:
            return False

        # Must be a straight line (row, column or exact diagonal) in an allowed direction
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False
        stepX, stepY = _sign(dx), _sign(dy)
        if (stepX, stepY) not in self.DIRECTIONS:
            return False

        # Every square between the start and the destination must be empty
        x, y = self.x + stepX, self.y + stepY
        while (x, y) != (newX, newY):
            if board.squares[x][y].isOccupied:
                return False
            x += stepX
            y += stepY

        return self.canLandOn(newX, newY, board)


ORTHOGONAL_DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
DIAGONAL_DIRECTIONS = ((1, 1), (1, -1), (-1, -1), (-1, 1))


def _sign(n):
    return (n > 0) - (n < 0)
