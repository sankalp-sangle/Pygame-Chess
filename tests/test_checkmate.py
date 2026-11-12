"""Check / checkmate detection in game.py."""
import pytest

import game
from Bishop import Bishop
from infra import ChessBoard
from King import King
from Pawn import Pawn
from Queen import Queen
from Rook import Rook


@pytest.fixture
def back_rank(place):
    """Black king on (0, 6) boxed in by its own pawns, white rook giving check along row 0."""
    blackKing = place(King, 0, 6, isWhite=False)
    for y in (5, 6, 7):
        place(Pawn, 1, y, isWhite=False)
    place(Rook, 0, 0, isWhite=True)
    whiteKing = place(King, 7, 7, isWhite=True)
    return blackKing, whiteKing


def test_back_rank_mate(board, back_rank):
    blackKing, _ = back_rank
    assert game.isCheckmate(board, False, blackKing)


def test_not_mate_if_king_can_step_out(board, back_rank):
    blackKing, _ = back_rank
    pawn = board.squares[1][7]
    pawn.piece, pawn.isOccupied = None, False
    assert not game.isCheckmate(board, False, blackKing)


def test_not_mate_if_checking_piece_can_be_captured(board, place, back_rank):
    blackKing, _ = back_rank
    place(Rook, 4, 0, isWhite=False)
    assert not game.isCheckmate(board, False, blackKing)


def test_not_mate_if_check_can_be_blocked(board, place, back_rank):
    blackKing, _ = back_rank
    place(Bishop, 2, 3, isWhite=False)   # can interpose on (0, 1) or (0, 5)
    assert not game.isCheckmate(board, False, blackKing)


def test_not_mate_without_check(board, back_rank):
    _, whiteKing = back_rank
    assert not game.isCheckmate(board, True, whiteKing)


def test_stalemate_is_not_checkmate(board, place):
    blackKing = place(King, 0, 0, isWhite=False)
    place(Queen, 2, 1, isWhite=True)
    place(King, 7, 7, isWhite=True)
    assert not game.kingUnderCheck(board, blackKing)
    assert not game.hasLegalMove(board, False, blackKing)
    assert not game.isCheckmate(board, False, blackKing)


def test_fools_mate_from_starting_position():
    board = ChessBoard(game.initializeBoard())
    game.initializePieces(board)
    whiteKing = board.squares[7][4].piece
    moves = [((6, 5), (5, 5)),   # f3
             ((1, 4), (3, 4)),   # e5
             ((6, 6), (4, 6)),   # g4
             ((0, 3), (4, 7))]   # Qh4#
    for (fromX, fromY), (toX, toY) in moves:
        piece = board.squares[fromX][fromY].piece
        assert piece is not None and piece.validate(toX, toY, board)
        game.movePiece(board, piece, toX, toY)
        board.lastPieceMoved = piece
    assert game.isCheckmate(board, True, whiteKing)


def test_search_leaves_board_and_flags_unchanged():
    board = ChessBoard(game.initializeBoard())
    game.initializePieces(board)
    before = [[(sq.piece, sq.isOccupied) for sq in row] for row in board.squares]
    whiteKing = board.squares[7][4].piece

    assert game.hasLegalMove(board, True, whiteKing)

    assert [[(sq.piece, sq.isOccupied) for sq in row] for row in board.squares] == before
    assert board.consideringEnPassant is False
    pawns = [sq.piece for row in board.squares for sq in row if isinstance(sq.piece, Pawn)]
    assert not any(p.jumpedTwoSquares for p in pawns)
    assert all(sq.piece is None or (sq.piece.x, sq.piece.y) == (sq.x, sq.y) for row in board.squares for sq in row)
