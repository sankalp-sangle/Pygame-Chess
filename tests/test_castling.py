"""Castling.

The king moves two squares towards a rook and that rook jumps to the square
the king crossed. Allowed only if neither piece has moved, every square
between them is empty, and the king is not in check, does not pass through
an attacked square and does not land on one.

Board-shape conditions are checked by King.validate(); conditions about
attacked squares need kingUnderCheck() and are checked by game.isLegalMove().
Each "not allowed" test first confirms castling is allowed in a clean setup,
so it can only pass for the right reason.
"""
from pathlib import Path
from types import SimpleNamespace

import pygame
import pytest

import game
from King import King
from Rook import Rook
from Knight import Knight
from Bishop import Bishop

SRC = Path(__file__).resolve().parent.parent / "src"

KINGSIDE, QUEENSIDE = "kingside", "queenside"
# column the king lands on, rook's corner column, column the rook lands on, squares that must be empty
SIDES = {
    KINGSIDE:  dict(kingTo=6, rookFrom=7, rookTo=5, between=(5, 6)),
    QUEENSIDE: dict(kingTo=2, rookFrom=0, rookTo=3, between=(1, 2, 3)),
}


@pytest.fixture(params=[True, False], ids=["white", "black"])
def isWhite(request):
    return request.param


@pytest.fixture
def setup(board, place, isWhite):
    """King and both rooks on their home squares, nothing else on the back rank."""
    row = 7 if isWhite else 0
    king = place(King, row, 4, isWhite)
    rooks = {KINGSIDE: place(Rook, row, 7, isWhite), QUEENSIDE: place(Rook, row, 0, isWhite)}
    # Kings are needed by isLegalMove(); keep the enemy one far from the action.
    place(King, 4 if isWhite else 3, 0, not isWhite)
    return SimpleNamespace(row=row, king=king, rooks=rooks, board=board)


def canCastle(s, side):
    """Both layers must accept the castle: King.validate() and game.isLegalMove()."""
    col = SIDES[side]["kingTo"]
    return s.king.validate(s.row, col, s.board) and game.isLegalMove(s.board, s.king, s.row, col, s.king)


def clear(board, x, y):
    board.squares[x][y].piece, board.squares[x][y].isOccupied = None, False


# ---------- allowed ----------

@pytest.mark.parametrize("side", [KINGSIDE, QUEENSIDE])
def test_castling_allowed_with_clear_back_rank(setup, side):
    assert canCastle(setup, side)


def test_castling_allowed_with_only_one_rook(setup):
    clear(setup.board, setup.row, 0)
    assert canCastle(setup, KINGSIDE)


def test_queenside_allowed_when_only_the_rook_crossing_square_is_attacked(setup, place, isWhite):
    # (row, 1) must be empty but may be attacked: only the king's path matters.
    place(Rook, 4, 1, not isWhite)
    assert canCastle(setup, QUEENSIDE)


# ---------- moved pieces ----------

def test_moved_king_cannot_castle(setup):
    assert canCastle(setup, KINGSIDE) and canCastle(setup, QUEENSIDE)
    setup.king.hasMoved = True
    assert not canCastle(setup, KINGSIDE)
    assert not canCastle(setup, QUEENSIDE)


@pytest.mark.parametrize("side, otherSide", [(KINGSIDE, QUEENSIDE), (QUEENSIDE, KINGSIDE)])
def test_moved_rook_blocks_only_its_own_side(setup, side, otherSide):
    assert canCastle(setup, side)
    setup.rooks[side].hasMoved = True
    assert not canCastle(setup, side)
    assert canCastle(setup, otherSide)


@pytest.mark.parametrize("side", [KINGSIDE, QUEENSIDE])
def test_missing_rook_cannot_castle(setup, side):
    assert canCastle(setup, side)
    clear(setup.board, setup.row, SIDES[side]["rookFrom"])
    assert not canCastle(setup, side)


@pytest.mark.parametrize("side", [KINGSIDE, QUEENSIDE])
def test_enemy_rook_in_corner_cannot_castle(setup, place, isWhite, side):
    assert canCastle(setup, side)
    place(Rook, setup.row, SIDES[side]["rookFrom"], not isWhite)
    assert not canCastle(setup, side)


# ---------- non-empty squares ----------

@pytest.mark.parametrize("side, col", [(KINGSIDE, 5), (KINGSIDE, 6), (QUEENSIDE, 1), (QUEENSIDE, 2), (QUEENSIDE, 3)])
@pytest.mark.parametrize("blockerIsEnemy", [False, True], ids=["own", "enemy"])
def test_piece_between_king_and_rook_blocks_castling(setup, place, isWhite, side, col, blockerIsEnemy):
    assert canCastle(setup, side)
    place(Bishop, setup.row, col, isWhite != blockerIsEnemy)
    assert not canCastle(setup, side)


# ---------- check ----------

@pytest.mark.parametrize("side", [KINGSIDE, QUEENSIDE])
def test_cannot_castle_out_of_check(setup, place, isWhite, side):
    assert canCastle(setup, side)
    place(Rook, 4 if not isWhite else 3, 4, not isWhite)   # attacks the king down column 4
    assert game.kingUnderCheck(setup.board, setup.king)
    assert not canCastle(setup, side)


@pytest.mark.parametrize("side, crossedCol", [(KINGSIDE, 5), (QUEENSIDE, 3)])
def test_cannot_castle_through_an_attacked_square(setup, place, isWhite, side, crossedCol):
    assert canCastle(setup, side)
    place(Rook, 4 if not isWhite else 3, crossedCol, not isWhite)
    assert not canCastle(setup, side)


@pytest.mark.parametrize("side", [KINGSIDE, QUEENSIDE])
def test_cannot_castle_into_check(setup, place, isWhite, side):
    assert canCastle(setup, side)
    place(Rook, 4 if not isWhite else 3, SIDES[side]["kingTo"], not isWhite)
    assert not canCastle(setup, side)


# ---------- playing it in the real game loop ----------

def play(monkeypatch, squares):
    """Run game.main() with clicks on the given (row, col) squares; return the final board."""
    monkeypatch.chdir(SRC)
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    clicks = iter([(col * game.SQUARE_SIZE + 50, row * game.SQUARE_SIZE + 50) for row, col in squares])
    script = [[SimpleNamespace(type=pygame.MOUSEBUTTONDOWN)] for _ in squares] + [[SimpleNamespace(type=pygame.QUIT)]]
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: next(clicks))
    monkeypatch.setattr(pygame.event, "get", lambda: script.pop(0))
    boards = []
    original = game.printBoard
    monkeypatch.setattr(game, "printBoard", lambda screen, board, *a: (boards.append(board), original(screen, board, *a)))
    game.main()
    return boards[-1]


# Clears white's kingside (e4, Nf3, Bc4) while black shuffles a knight.
CLEAR_WHITE_KINGSIDE = [
    (6, 4), (4, 4),  (0, 1), (2, 2),   # e4      Nc6
    (7, 6), (5, 5),  (2, 2), (0, 1),   # Nf3     Nb8
    (7, 5), (4, 2),  (0, 1), (2, 2),   # Bc4     Nc6
]


def test_castling_by_clicking_moves_king_and_rook(monkeypatch):
    board = play(monkeypatch, CLEAR_WHITE_KINGSIDE + [(7, 4), (7, 6)])
    assert isinstance(board.squares[7][6].piece, King)
    assert isinstance(board.squares[7][5].piece, Rook)
    assert board.squares[7][4].piece is None and board.squares[7][7].piece is None


def test_king_that_moved_and_returned_cannot_castle(monkeypatch):
    kingOutAndBack = [(7, 4), (7, 5),  (2, 2), (0, 1),   # Ke1-f1   Nb8
                      (7, 5), (7, 4),  (0, 1), (2, 2)]   # Kf1-e1   Nc6
    board = play(monkeypatch, CLEAR_WHITE_KINGSIDE + kingOutAndBack + [(7, 4), (7, 6)])
    assert isinstance(board.squares[7][4].piece, King)
    assert isinstance(board.squares[7][7].piece, Rook)
