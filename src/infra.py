from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame

    from Piece import Piece


# eq=False: squares and boards are identities, not values. Two empty light
# squares must not compare equal, and both must stay hashable.

@dataclass(eq=False)
class ChessBoard:
    squares: list[list[Square]] = field(default_factory=list, repr=False)
    lastPieceMoved: Piece | None = None
    consideringEnPassant: bool = False


@dataclass(eq=False)
class Square:
    isWhite: bool = False
    isOccupied: bool = False
    x: int = 0
    y: int = 0
    piece: Piece | None = None
    image: pygame.Surface | None = field(default=None, repr=False)

    @property
    def image_path(self) -> str:
        return "../img/white.png" if self.isWhite else "../img/black.png"
