"""Rook, Bishop and Queen: slide any distance along their directions until blocked."""
import pytest

from Rook import Rook
from Bishop import Bishop
from Queen import Queen
from Knight import Knight

SLIDING = [Rook, Bishop, Queen]


def sign(n):
    return (n > 0) - (n < 0)


def ray(start, direction):
    """All on-board squares from `start` (exclusive) in `direction`."""
    (x, y), (dx, dy) = start, direction
    squares = []
    x, y = x + dx, y + dy
    while 0 <= x < 8 and 0 <= y < 8:
        squares.append((x, y))
        x, y = x + dx, y + dy
    return squares


def expected_targets(cls, start):
    return {sq for d in cls.DIRECTIONS for sq in ray(start, d)}


# ---------- happy path: full move sets on an empty board ----------

@pytest.mark.parametrize("cls", SLIDING)
@pytest.mark.parametrize("start", [(3, 3), (0, 0), (7, 7), (0, 4), (4, 7)])
def test_empty_board_move_set(place, targets, cls, start):
    piece = place(cls, *start)
    assert targets(piece) == expected_targets(cls, start)


@pytest.mark.parametrize("cls, start, count", [
    (Rook,   (3, 3), 14),
    (Rook,   (0, 0), 14),   # a rook always sees 14 squares on an empty board
    (Bishop, (3, 3), 13),
    (Bishop, (0, 0), 7),    # corner: only one diagonal
    (Bishop, (0, 3), 7),    # edge
    (Queen,  (3, 3), 27),
    (Queen,  (0, 0), 21),
])
def test_empty_board_move_count(place, targets, cls, start, count):
    assert len(targets(place(cls, *start))) == count


@pytest.mark.parametrize("isWhite", [True, False])
def test_black_and_white_move_the_same(place, targets, isWhite):
    queen = place(Queen, 4, 4, isWhite)
    assert targets(queen) == expected_targets(Queen, (4, 4))


# ---------- invalid shapes ----------

@pytest.mark.parametrize("cls, target", [
    (Rook,   (4, 4)),   # diagonal
    (Rook,   (5, 4)),   # knight-shaped
    (Bishop, (3, 6)),   # along a row
    (Bishop, (6, 3)),   # along a column
    (Bishop, (5, 6)),   # not an exact diagonal
    (Queen,  (5, 4)),   # knight-shaped
    (Queen,  (6, 4)),   # off-diagonal
])
def test_rejects_moves_outside_its_directions(board, place, cls, target):
    piece = place(cls, 3, 3)
    assert piece.validate(*target, board) is False


# ---------- blocking and capturing ----------

@pytest.mark.parametrize("cls, blocker", [
    (Rook,   (3, 5)),
    (Bishop, (5, 5)),
    (Queen,  (3, 5)),
    (Queen,  (5, 5)),
])
def test_own_piece_blocks_its_square_and_beyond(board, place, cls, blocker):
    piece = place(cls, 3, 3, isWhite=True)
    place(Knight, *blocker, isWhite=True)
    line = ray((3, 3), (sign(blocker[0] - 3), sign(blocker[1] - 3)))
    before = line[:line.index(blocker)]
    after = line[line.index(blocker):]
    assert all(piece.validate(*sq, board) for sq in before)
    assert not any(piece.validate(*sq, board) for sq in after)


@pytest.mark.parametrize("cls, blocker, beyond", [
    (Rook,   (3, 5), (3, 6)),
    (Bishop, (5, 5), (6, 6)),
    (Queen,  (1, 1), (0, 0)),
])
def test_enemy_piece_can_be_captured_but_not_jumped(board, place, cls, blocker, beyond):
    piece = place(cls, 3, 3, isWhite=True)
    place(Knight, *blocker, isWhite=False)
    assert piece.validate(*blocker, board)
    assert not piece.validate(*beyond, board)


@pytest.mark.parametrize("cls, neighbour", [
    (Rook,   (3, 4)),
    (Bishop, (4, 4)),
    (Queen,  (2, 3)),
])
def test_adjacent_own_piece_blocks_whole_direction(board, place, targets, cls, neighbour):
    piece = place(cls, 3, 3)
    place(Knight, *neighbour)
    direction = (neighbour[0] - 3, neighbour[1] - 3)
    assert targets(piece).isdisjoint(ray((3, 3), direction))


def test_fully_surrounded_queen_has_no_moves(place, targets):
    queen = place(Queen, 3, 3)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                place(Knight, 3 + dx, 3 + dy)
    assert targets(queen) == set()


def test_fully_surrounded_by_enemies_queen_can_capture_each(place, targets):
    queen = place(Queen, 3, 3, isWhite=True)
    neighbours = {(3 + dx, 3 + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy}
    for sq in neighbours:
        place(Knight, *sq, isWhite=False)
    assert targets(queen) == neighbours
