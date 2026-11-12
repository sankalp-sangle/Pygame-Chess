"""Pawn: forward moves, the opening double step, diagonal captures and en passant.

White pawns start on row 6 and move towards row 0; black pawns start on row 1
and move towards row 7. Most tests run once per colour using `side`.
"""
import pytest

from Pawn import Pawn
from Rook import Rook


class Side:
    def __init__(self, isWhite):
        self.isWhite = isWhite
        self.forward = -1 if isWhite else 1
        self.startRow = 6 if isWhite else 1
        # Row where this side's pawn can capture en passant, and where an enemy
        # pawn lands after its double step next to it.
        self.enPassantRow = 3 if isWhite else 4

    def __repr__(self):
        return "white" if self.isWhite else "black"


@pytest.fixture(params=[True, False], ids=["white", "black"])
def side(request):
    return Side(request.param)


def ahead(side, x, steps):
    return x + side.forward * steps


# ---------- happy path ----------

def test_one_step_forward(board, place, side):
    pawn = place(Pawn, side.startRow, 3, side.isWhite)
    assert pawn.validate(ahead(side, side.startRow, 1), 3, board)


def test_double_step_from_start_row(board, place, side):
    pawn = place(Pawn, side.startRow, 3, side.isWhite)
    assert pawn.validate(ahead(side, side.startRow, 2), 3, board)
    assert pawn.jumpedTwoSquares is True


@pytest.mark.parametrize("dy", [-1, 1])
def test_diagonal_capture(board, place, side, dy):
    pawn = place(Pawn, 4, 3, side.isWhite)
    place(Rook, ahead(side, 4, 1), 3 + dy, not side.isWhite)
    assert pawn.validate(ahead(side, 4, 1), 3 + dy, board)


def test_full_move_set_from_start_row_with_captures_available(place, targets, side):
    pawn = place(Pawn, side.startRow, 3, side.isWhite)
    one = ahead(side, side.startRow, 1)
    place(Rook, one, 2, not side.isWhite)
    place(Rook, one, 4, not side.isWhite)
    assert targets(pawn) == {(one, 3), (ahead(side, side.startRow, 2), 3), (one, 2), (one, 4)}


# ---------- boundary cases ----------

def test_double_step_only_from_start_row(board, place, side):
    row = ahead(side, side.startRow, 1)
    pawn = place(Pawn, row, 3, side.isWhite)
    assert pawn.validate(ahead(side, row, 2), 3, board) is False


def test_single_step_does_not_set_jumped_flag(board, place, side):
    pawn = place(Pawn, side.startRow, 3, side.isWhite)
    pawn.validate(ahead(side, side.startRow, 1), 3, board)
    assert pawn.jumpedTwoSquares is False


@pytest.mark.parametrize("blocked_steps", [1, 2])
def test_double_step_blocked(board, place, side, blocked_steps):
    pawn = place(Pawn, side.startRow, 3, side.isWhite)
    place(Rook, ahead(side, side.startRow, blocked_steps), 3, not side.isWhite)
    assert pawn.validate(ahead(side, side.startRow, 2), 3, board) is False
    assert pawn.jumpedTwoSquares is False


@pytest.mark.parametrize("blocker_is_enemy", [True, False])
def test_cannot_capture_straight_ahead(board, place, side, blocker_is_enemy):
    pawn = place(Pawn, 4, 3, side.isWhite)
    place(Rook, ahead(side, 4, 1), 3, side.isWhite != blocker_is_enemy)
    assert pawn.validate(ahead(side, 4, 1), 3, board) is False


@pytest.mark.parametrize("y, capture_y", [(0, 1), (7, 6)])
def test_edge_file_pawn_captures_inwards(board, place, side, y, capture_y):
    pawn = place(Pawn, 4, y, side.isWhite)
    place(Rook, ahead(side, 4, 1), capture_y, not side.isWhite)
    assert pawn.validate(ahead(side, 4, 1), capture_y, board)


# ---------- invalid moves ----------

def test_cannot_move_diagonally_onto_empty_square(board, place, side):
    pawn = place(Pawn, 4, 3, side.isWhite)
    assert pawn.validate(ahead(side, 4, 1), 4, board) is False


def test_cannot_capture_own_piece(board, place, side):
    pawn = place(Pawn, 4, 3, side.isWhite)
    place(Rook, ahead(side, 4, 1), 4, side.isWhite)
    assert pawn.validate(ahead(side, 4, 1), 4, board) is False


@pytest.mark.parametrize("dx, dy", [
    (-1, 0),   # backwards
    (0, 1),    # sideways
    (-1, 1),   # diagonally backwards
    (3, 0),    # three squares forward
    (2, 1),    # knight-shaped
])
def test_rejects_illegal_shapes(board, place, side, dx, dy):
    pawn = place(Pawn, 4, 3, side.isWhite)
    # Put enemies everywhere so captures can't make a move legal by accident.
    for x in range(8):
        for y in range(8):
            if (x, y) != (4, 3):
                place(Rook, x, y, not side.isWhite)
    assert pawn.validate(ahead(side, 4, dx), 3 + dy, board) is False


@pytest.mark.xfail(reason="Pawn.validate() wraps column -1 around to column 7")
def test_edge_file_pawn_cannot_capture_off_board(board, place, side):
    pawn = place(Pawn, 4, 0, side.isWhite)
    place(Rook, ahead(side, 4, 1), 7, not side.isWhite)
    assert pawn.validate(ahead(side, 4, 1), -1, board) is False


# ---------- en passant ----------

def enemy_double_step(board, place, side, y):
    """Place an enemy pawn as if it had just double-stepped to land on column y."""
    enemy = place(Pawn, side.enPassantRow, y, not side.isWhite)
    enemy.jumpedTwoSquares = True
    board.lastPieceMoved = enemy
    return enemy


@pytest.mark.parametrize("dy", [-1, 1])
def test_en_passant(board, place, side, dy):
    pawn = place(Pawn, side.enPassantRow, 3, side.isWhite)
    enemy_double_step(board, place, side, 3 + dy)
    assert pawn.validate(ahead(side, side.enPassantRow, 1), 3 + dy, board)
    assert board.consideringEnPassant is True


def test_no_en_passant_after_single_step(board, place, side):
    pawn = place(Pawn, side.enPassantRow, 3, side.isWhite)
    enemy = enemy_double_step(board, place, side, 4)
    enemy.jumpedTwoSquares = False
    assert pawn.validate(ahead(side, side.enPassantRow, 1), 4, board) is False
    assert board.consideringEnPassant is False


def test_no_en_passant_if_another_piece_moved_last(board, place, side):
    pawn = place(Pawn, side.enPassantRow, 3, side.isWhite)
    enemy_double_step(board, place, side, 4)
    board.lastPieceMoved = place(Rook, 0 if side.isWhite else 7, 0, not side.isWhite)
    assert pawn.validate(ahead(side, side.enPassantRow, 1), 4, board) is False


def test_no_en_passant_from_wrong_row(board, place, side):
    row = ahead(side, side.enPassantRow, 1)
    pawn = place(Pawn, row, 3, side.isWhite)
    enemy_double_step(board, place, side, 4)
    assert pawn.validate(ahead(side, row, 1), 4, board) is False


@pytest.mark.xfail(reason="Pawn.validate() does not check the captured pawn is on an adjacent column")
def test_no_en_passant_from_distant_column(board, place, side):
    pawn = place(Pawn, side.enPassantRow, 0, side.isWhite)
    enemy_double_step(board, place, side, 5)
    assert pawn.validate(ahead(side, side.enPassantRow, 1), 5, board) is False
