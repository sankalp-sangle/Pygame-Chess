"""Shared behaviour from the Piece base class, checked across every piece type."""
import pytest

from Piece import Piece
from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn

ALL_PIECES = [King, Queen, Rook, Bishop, Knight, Pawn]


def test_base_piece_validate_is_abstract(board):
    with pytest.raises(NotImplementedError):
        Piece(x=0, y=0, square=board.squares[0][0], isWhite=True).validate(1, 1, board)


@pytest.mark.parametrize("cls", ALL_PIECES)
def test_constructor_sets_position_colour_and_sprite_size(board, cls):
    square = board.squares[2][5]
    piece = cls(x=2, y=5, square=square, isWhite=False, path="img.png")
    assert (piece.x, piece.y, piece.square, piece.isWhite, piece.image_path) == (2, 5, square, False, "img.png")
    assert piece.width == 96
    assert piece.height > 0


@pytest.mark.parametrize("cls", ALL_PIECES)
@pytest.mark.parametrize("isWhite", [True, False])
def test_cannot_move_to_own_square(board, place, cls, isWhite):
    piece = place(cls, 3, 3, isWhite)
    assert piece.validate(3, 3, board) is False


class TestCanLandOn:
    def test_empty_square(self, board, place):
        rook = place(Rook, 0, 0)
        assert rook.canLandOn(0, 5, board)

    def test_enemy_piece(self, board, place):
        rook = place(Rook, 0, 0, isWhite=True)
        place(Knight, 0, 5, isWhite=False)
        assert rook.canLandOn(0, 5, board)

    def test_own_piece(self, board, place):
        rook = place(Rook, 0, 0, isWhite=True)
        place(Knight, 0, 5, isWhite=True)
        assert not rook.canLandOn(0, 5, board)


# validate() does no bounds check: negative indices wrap around to the other
# side of the board, and indices >= 8 raise IndexError. The game never passes
# off-board coordinates today (clicks are always on the board), but move
# generation will. Remove the xfail once validate() rejects them.
@pytest.mark.xfail(reason="validate() does not reject off-board coordinates")
@pytest.mark.parametrize("cls, start, target", [
    (Rook,   (0, 0), (-1, 0)),
    (Rook,   (7, 0), (8, 0)),
    (Bishop, (0, 0), (-1, -1)),
    (Queen,  (7, 7), (8, 8)),
    (Knight, (0, 0), (-1, -2)),
    (King,   (0, 0), (-1, -1)),
])
def test_off_board_target_is_rejected(board, place, cls, start, target):
    piece = place(cls, *start)
    assert piece.validate(*target, board) is False
