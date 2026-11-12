from Piece import SteppingPiece


class Knight(SteppingPiece):
    HEIGHT = 75
    OFFSETS = ((1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1), (-2, 1), (-1, 2))
