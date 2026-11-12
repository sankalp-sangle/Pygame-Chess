from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame

    from infra import ChessBoard, Square

Offset = tuple[int, int]


class Piece:
    # Sprite size in pixels, used to center the image on its square. Overridden per piece.
    HEIGHT = 0
    WIDTH = 96

    def __init__(self, x: int, y: int, square: Square, isWhite: bool, path: str = ""):
        self.x = x
        self.y = y
        self.image_path = path
        self.image: pygame.Surface | None = None
        self.square = square
        self.height = self.HEIGHT
        self.width = self.WIDTH
        self.isWhite = isWhite
        self.hasMoved = False   # set once the piece makes a move in the game; used for castling

    def validate(self, newX: int, newY: int, board: ChessBoard) -> bool:
        raise NotImplementedError

    def canLandOn(self, newX: int, newY: int, board: ChessBoard) -> bool:
        # A piece can land on an empty square or capture a piece of the other colour
        return not board.squares[newX][newY].isOccupied or self.isEnemyAt(newX, newY, board)

    def isEnemyAt(self, newX: int, newY: int, board: ChessBoard) -> bool:
        target = board.squares[newX][newY].piece
        return target is not None and target.isWhite != self.isWhite


class SteppingPiece(Piece):
    # Pieces that jump straight to one of a fixed set of offsets (King, Knight)
    OFFSETS: tuple[Offset, ...] = ()

    def validate(self, newX: int, newY: int, board: ChessBoard) -> bool:
        if (newX - self.x, newY - self.y) not in self.OFFSETS:
            return False
        return self.canLandOn(newX, newY, board)


class SlidingPiece(Piece):
    # Pieces that slide any distance along a set of directions until blocked (Rook, Bishop, Queen)
    DIRECTIONS: tuple[Offset, ...] = ()

    def validate(self, newX: int, newY: int, board: ChessBoard) -> bool:
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


ORTHOGONAL_DIRECTIONS: tuple[Offset, ...] = ((0, 1), (1, 0), (0, -1), (-1, 0))
DIAGONAL_DIRECTIONS: tuple[Offset, ...] = ((1, 1), (1, -1), (-1, -1), (-1, 1))


def _sign(n: int) -> int:
    return (n > 0) - (n < 0)
