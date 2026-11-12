import pytest

from infra import ChessBoard, Square


@pytest.fixture
def board():
    """An empty 8x8 board."""
    return ChessBoard([[Square((x + y) % 2 == 0, x=x, y=y) for y in range(8)] for x in range(8)])


@pytest.fixture
def place(board):
    """Put a piece of class `cls` on (x, y) of `board` and return it."""
    def _place(cls, x, y, isWhite=True):
        square = board.squares[x][y]
        piece = cls(x=x, y=y, square=square, isWhite=isWhite)
        square.piece = piece
        square.isOccupied = True
        return piece
    return _place


@pytest.fixture
def targets(board):
    """Every on-board square the piece may move to, as a set of (x, y)."""
    def _targets(piece):
        return {(x, y) for x in range(8) for y in range(8) if piece.validate(x, y, board)}
    return _targets
