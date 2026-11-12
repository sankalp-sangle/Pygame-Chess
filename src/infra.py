from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame
    from Piece import Piece


class ChessBoard:
    def __init__(self, squares: list[list[Square]] | None = None):
        self.squares: list[list[Square]] = squares if squares is not None else []
        self.lastPieceMoved: Piece | None = None
        self.consideringEnPassant = False

class Square:
    def __init__(self, isWhite: bool = False, isOccupied: bool = False, x: int = 0, y: int = 0, piece: Piece | None = None):
        self.isWhite = isWhite
        self.isOccupied = isOccupied
        self.x = x
        self.y = y
        self.piece = piece
        self.image: pygame.Surface | None = None

        if isWhite:
            self.image_path = "../img/white.png"
        else:
            self.image_path = "../img/black.png"
