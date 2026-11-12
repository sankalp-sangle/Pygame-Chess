"""King and Knight: jump straight to one of a fixed set of offsets."""
import pytest

from King import King
from Knight import Knight
from Rook import Rook


def on_board(squares):
    return {(x, y) for x, y in squares if 0 <= x < 8 and 0 <= y < 8}


# ---------- happy path ----------

@pytest.mark.parametrize("cls", [King, Knight])
@pytest.mark.parametrize("start", [(3, 3), (0, 0), (7, 7), (0, 4), (4, 7), (1, 1)])
def test_empty_board_move_set(place, targets, cls, start):
    piece = place(cls, *start)
    x, y = start
    expected = on_board((x + dx, y + dy) for dx, dy in cls.OFFSETS)
    assert targets(piece) == expected


@pytest.mark.parametrize("cls, start, count", [
    (King,   (3, 3), 8),
    (King,   (0, 3), 5),   # edge
    (King,   (0, 0), 3),   # corner
    (Knight, (3, 3), 8),
    (Knight, (0, 3), 4),   # edge
    (Knight, (0, 0), 2),   # corner
    (Knight, (1, 1), 4),   # one in from the corner
])
def test_empty_board_move_count(place, targets, cls, start, count):
    assert len(targets(place(cls, *start))) == count


# ---------- invalid shapes ----------

@pytest.mark.parametrize("target", [(5, 3), (3, 5), (5, 5), (4, 5)])
def test_king_cannot_move_more_than_one_square(board, place, target):
    king = place(King, 3, 3)
    assert king.validate(*target, board) is False


@pytest.mark.parametrize("target", [(4, 4), (3, 4), (5, 5), (3, 5), (6, 4)])
def test_knight_rejects_non_l_shapes(board, place, target):
    knight = place(Knight, 3, 3)
    assert knight.validate(*target, board) is False


# ---------- capturing / own pieces ----------

@pytest.mark.parametrize("cls, target", [(King, (4, 4)), (Knight, (5, 4))])
def test_can_capture_enemy(board, place, cls, target):
    piece = place(cls, 3, 3, isWhite=True)
    place(Rook, *target, isWhite=False)
    assert piece.validate(*target, board)


@pytest.mark.parametrize("cls, target", [(King, (4, 4)), (Knight, (5, 4))])
def test_cannot_land_on_own_piece(board, place, cls, target):
    piece = place(cls, 3, 3, isWhite=False)
    place(Rook, *target, isWhite=False)
    assert piece.validate(*target, board) is False


def test_knight_jumps_over_surrounding_pieces(place, targets):
    knight = place(Knight, 3, 3)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                place(Rook, 3 + dx, 3 + dy)
    assert len(targets(knight)) == 8
