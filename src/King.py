from __future__ import annotations

from typing import TYPE_CHECKING

from Piece import DIAGONAL_DIRECTIONS, ORTHOGONAL_DIRECTIONS, SteppingPiece
from Rook import Rook

if TYPE_CHECKING:
    from infra import ChessBoard


class King(SteppingPiece):
    HEIGHT = 90
    OFFSETS = ORTHOGONAL_DIRECTIONS + DIAGONAL_DIRECTIONS

    def validate(self, newX: int, newY: int, board: ChessBoard) -> bool:
        return super().validate(newX, newY, board) or self.canCastle(newX, newY, board)

    def canCastle(self, newX: int, newY: int, board: ChessBoard) -> bool:
        # Board-shape rules only. Whether the king is in check, or would pass
        # through or land on an attacked square, is checked by game.isLegalMove().
        if self.hasMoved or newX != self.x or abs(newY - self.y) != 2:
            return False

        rookCol = 7 if newY > self.y else 0
        rook = board.squares[self.x][rookCol].piece
        if not isinstance(rook, Rook) or rook.isWhite != self.isWhite or rook.hasMoved:
            return False

        # Every square between the king and the rook must be empty
        step = 1 if rookCol > self.y else -1
        return all(not board.squares[self.x][y].isOccupied for y in range(self.y + step, rookCol, step))
