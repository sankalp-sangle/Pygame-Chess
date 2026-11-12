# Import the pygame module
import functools

import pygame

from infra import ChessBoard, Square
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn
from Piece import Piece

SQUARE_SIZE   = 100
NO_OF_SQUARES = 8
HIGHLIGHT_COLOUR = (0, 200, 0)
HIGHLIGHT_WIDTH  = 4
OVERLAY_COLOUR   = (0, 0, 0, 150)    # translucent black over the board when the game ends
BANNER_COLOUR    = (220, 30, 30)

# Initialize pygame
pygame.init()

def initializeBoard():
    board = [ [] for x in range(8) ]
    parity = 0
    row_number = 0
    for row in board:
        for column_number in range(NO_OF_SQUARES):
            board[row_number].append(Square(False if (parity + row_number) & 1 else True, isOccupied = True if row_number in [0,1,6,7] else False, x = row_number, y = column_number))
            parity += 1
        row_number += 1

    return board

def initializePieces(board):
    row = 1
    for col in range(8):
        board.squares[row][col].piece = Pawn(x = row, y = col, path = '../img/black/pawn.png', square = board.squares[row][col], isWhite = False)

    row = 0
    board.squares[row][0].piece = Rook(x = row, y = 0, path = '../img/black/rook.png', square = board.squares[row][0], isWhite = False)
    board.squares[row][7].piece = Rook(x = row, y = 7, path = '../img/black/rook.png', square = board.squares[row][7], isWhite = False)
    board.squares[row][1].piece = Knight(x = row, y = 1, path = '../img/black/knight.png', square = board.squares[row][1], isWhite = False)
    board.squares[row][6].piece = Knight(x = row, y = 6, path = '../img/black/knight.png', square = board.squares[row][6], isWhite = False)
    board.squares[row][2].piece = Bishop(x = row, y = 2, path = '../img/black/bishop.png', square = board.squares[row][2], isWhite = False)
    board.squares[row][5].piece = Bishop(x = row, y = 5, path = '../img/black/bishop.png', square = board.squares[row][5], isWhite = False)
    board.squares[row][3].piece = Queen(x = row, y = 3, path = '../img/black/queen.png', square = board.squares[row][3], isWhite = False)
    board.squares[row][4].piece = King(x = row, y = 4, path = '../img/black/king.png', square = board.squares[row][4], isWhite = False)

    row = 6
    for col in range(8):
        board.squares[row][col].piece = Pawn(x = row, y = col, path = '../img/white/pawn.png', square = board.squares[row][col], isWhite = True)

    row = 7
    board.squares[row][0].piece = Rook(x = row, y = 0, path = '../img/white/rook.png', square = board.squares[row][0], isWhite = True)
    board.squares[row][7].piece = Rook(x = row, y = 7, path = '../img/white/rook.png', square = board.squares[row][7], isWhite = True)
    board.squares[row][1].piece = Knight(x = row, y = 1, path = '../img/white/knight.png', square = board.squares[row][1], isWhite = True)
    board.squares[row][6].piece = Knight(x = row, y = 6, path = '../img/white/knight.png', square = board.squares[row][6], isWhite = True)
    board.squares[row][2].piece = Bishop(x = row, y = 2, path = '../img/white/bishop.png', square = board.squares[row][2], isWhite = True)
    board.squares[row][5].piece = Bishop(x = row, y = 5, path = '../img/white/bishop.png', square = board.squares[row][5], isWhite = True)
    board.squares[row][3].piece = Queen(x = row, y = 3, path = '../img/white/queen.png', square = board.squares[row][3], isWhite = True)
    board.squares[row][4].piece = King(x = row, y = 4, path = '../img/white/king.png', square = board.squares[row][4], isWhite = True)



def kingUnderCheck(board, king):
    x , y = king.x, king.y

    # Check for pawns
    if king.isWhite:
        if x-1 >= 0 and y-1 >= 0 and board.squares[x-1][y-1].isOccupied and isinstance(board.squares[x-1][y-1].piece, Pawn) and not board.squares[x-1][y-1].piece.isWhite:
            return True
        if x-1 >= 0 and y+1 < NO_OF_SQUARES and board.squares[x-1][y+1].isOccupied and isinstance(board.squares[x-1][y+1].piece, Pawn) and not board.squares[x-1][y+1].piece.isWhite:
            return True
    else:
        if x+1 < NO_OF_SQUARES and y+1 < NO_OF_SQUARES and board.squares[x+1][y+1].isOccupied and isinstance(board.squares[x+1][y+1].piece, Pawn) and board.squares[x+1][y+1].piece.isWhite:
            return True
        if x+1 < NO_OF_SQUARES and y-1 >= 0 and board.squares[x+1][y-1].isOccupied and isinstance(board.squares[x+1][y-1].piece, Pawn) and board.squares[x+1][y-1].piece.isWhite:
            return True

    # Check for knights
    DANGER_POSITIONS = [[1, 2], [2, 1], [-1, -2], [-2, -1], [1, -2], [2, -1], [-2, 1], [-1, 2]]
    for [addX, addY] in DANGER_POSITIONS:
        checkX = addX + x
        checkY = addY + y
        if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
            continue
        if board.squares[checkX][checkY].isOccupied and isinstance(board.squares[checkX][checkY].piece, Knight) and board.squares[checkX][checkY].piece.isWhite != king.isWhite:
            return True
    
    # Check in vertical directions for Queens or Rooks of different colour
    VERTICAL_DIRECTIONS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    for [addX, addY] in VERTICAL_DIRECTIONS:
        checkX, checkY = addX + x, addY + y
        while checkX >= 0 and checkX <= 7 and checkY >= 0 and checkY <= 7 and not board.squares[checkX][checkY].isOccupied:
            checkX += addX
            checkY += addY
        if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
            continue
        else:
            if (isinstance(board.squares[checkX][checkY].piece, Rook) or isinstance(board.squares[checkX][checkY].piece, Queen)) and board.squares[checkX][checkY].piece.isWhite != king.isWhite:
                return True

    # Check in diagonal directions for Queens or Bishops of different colour
    DIAGONAL_DIRECTIONS = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
    for [addX, addY] in DIAGONAL_DIRECTIONS:
        checkX, checkY = addX + x, addY + y
        while checkX >= 0 and checkX <= 7 and checkY >= 0 and checkY <= 7 and not board.squares[checkX][checkY].isOccupied:
            checkX += addX
            checkY += addY
        if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
            continue
        else:
            if (isinstance(board.squares[checkX][checkY].piece, Bishop) or isinstance(board.squares[checkX][checkY].piece, Queen)) and board.squares[checkX][checkY].piece.isWhite != king.isWhite:
                return True

    # Check for King of different colour
    KING_DIRECTIONS = [[1,1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]
    for [addX, addY] in KING_DIRECTIONS:
        checkX, checkY = addX + x, addY + y
        if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
            continue
        else:
            if isinstance(board.squares[checkX][checkY].piece, King):
                return True

    return False

def movePiece(board, piece, row, col):
    """Move `piece` to (row, col), replacing whatever was there. Returns the captured piece, if any."""
    oldSquare, newSquare = piece.square, board.squares[row][col]
    captured = newSquare.piece
    oldSquare.piece, oldSquare.isOccupied = None, False
    newSquare.piece, newSquare.isOccupied = piece, True
    piece.square, piece.x, piece.y = newSquare, row, col
    return captured

def leavesKingInCheck(board, piece, row, col, king, enPassantVictim=None):
    """Try the move, test whether `king` is attacked, then put everything back."""
    oldSquare = piece.square
    if enPassantVictim is not None:
        enPassantVictim.square.piece, enPassantVictim.square.isOccupied = None, False
    captured = movePiece(board, piece, row, col)

    inCheck = kingUnderCheck(board, king)

    newSquare = piece.square
    movePiece(board, piece, oldSquare.x, oldSquare.y)
    newSquare.piece, newSquare.isOccupied = captured, captured is not None
    if enPassantVictim is not None:
        enPassantVictim.square.piece, enPassantVictim.square.isOccupied = enPassantVictim, True
    return inCheck

def hasLegalMove(board, isWhite, king):
    """True if the side `isWhite` has at least one move that doesn't leave its king in check."""
    pieces = [square.piece for row in board.squares for square in row
              if square.piece is not None and square.piece.isWhite == isWhite]
    for piece in pieces:
        for row in range(NO_OF_SQUARES):
            for col in range(NO_OF_SQUARES):
                # Pawn.validate() sets flags as a side effect, so save and restore them
                savedEnPassant = board.consideringEnPassant
                savedJumped = piece.jumpedTwoSquares if isinstance(piece, Pawn) else False
                valid = piece.validate(row, col, board)
                isEnPassant = board.consideringEnPassant and not savedEnPassant
                board.consideringEnPassant = savedEnPassant
                if isinstance(piece, Pawn):
                    piece.jumpedTwoSquares = savedJumped

                victim = board.lastPieceMoved if isEnPassant else None
                if valid and not leavesKingInCheck(board, piece, row, col, king, victim):
                    return True
    return False

def isCheckmate(board, isWhite, king):
    """True if the side `isWhite` is in check and has no legal move."""
    return kingUnderCheck(board, king) and not hasLegalMove(board, isWhite, king)

def main():
    screen = pygame.display.set_mode((SQUARE_SIZE * 8, SQUARE_SIZE * 8))

    pygame.display.set_caption("Sankalp Chess")
    icon = pygame.image.load('../img/chess.png')
    pygame.display.set_icon(icon)

    board = ChessBoard()
    board.squares = initializeBoard()
    initializePieces(board)

    whiteKing = board.squares[7][4].piece
    blackKing = board.squares[0][4].piece
    assert isinstance(whiteKing, King) and isinstance(blackKing, King)

    for row in range(len(board.squares)):
        for col in range(len(board.squares[0])):
            square = board.squares[row][col]
            square.image = pygame.image.load(square.image_path)
            if square.piece:
                square.piece.image = pygame.image.load(square.piece.image_path)
            
    isWhiteTurn = True

    state_running = True

    selectedPiece: Piece | None = None
    gameOver = False

    while state_running:
        printBoard(screen, board, selectedPiece.square if selectedPiece else None,
                   "CHECKMATE" if gameOver else None)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                (x, y) = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if selectedPiece is None:
                    # Only the side to move can select a piece
                    clickedPiece = board.squares[row][col].piece
                    if clickedPiece is not None and clickedPiece.isWhite == isWhiteTurn:
                        selectedPiece = clickedPiece
                elif selectedPiece.square is board.squares[row][col]:
                    # Clicking the selected square again deselects it
                    selectedPiece = None
                else:
                    decision = (isWhiteTurn == selectedPiece.isWhite) and selectedPiece.validate(row, col, board)
                    if decision:
                        # Reject the move if it would leave the mover's king in check
                        enPassantVictim = board.lastPieceMoved if board.consideringEnPassant else None
                        if leavesKingInCheck(board, selectedPiece, row, col, whiteKing if isWhiteTurn else blackKing, enPassantVictim):
                            board.consideringEnPassant = False
                        else:
                            movePiece(board, selectedPiece, row, col)

                            # Check for pawn promotion
                            if isinstance(selectedPiece, Pawn) and ((selectedPiece.isWhite and selectedPiece.x == 0) or (not selectedPiece.isWhite and selectedPiece.x == 7)):
                                selectedPiece.square.piece = Queen(x = selectedPiece.x, y = selectedPiece.y, path = '../img/' + ('white' if selectedPiece.isWhite else 'black') + '/queen.png', square = selectedPiece.square, isWhite = selectedPiece.isWhite)
                                selectedPiece = selectedPiece.square.piece
                                selectedPiece.image = pygame.image.load(selectedPiece.image_path)

                            # After successful move, flip turn variable
                            isWhiteTurn = not isWhiteTurn

                            # If an En Passant move, remove the captured pawn
                            if board.consideringEnPassant and board.lastPieceMoved is not None:
                                board.lastPieceMoved.square.piece = None
                                board.lastPieceMoved.square.isOccupied = False
                                board.consideringEnPassant = False

                            # Update last piece moved
                            board.lastPieceMoved = selectedPiece

                            # The side now to move is checkmated if it's in check with no legal move
                            gameOver = isCheckmate(board, isWhiteTurn, whiteKing if isWhiteTurn else blackKing)

                    # Remove selected piece
                    selectedPiece = None
                    
        pygame.display.update()

def printBoard(screen, board, selectedSquare=None, message=None):
    for row in range(len(board.squares)):
        for col in range(len(board.squares[0])):
            square = board.squares[row][col]
            assert square.image is not None, "square images are loaded in main()"
            screen.blit(square.image, (square.y * SQUARE_SIZE, square.x * SQUARE_SIZE))       
            if square.piece:
                assert square.piece.image is not None, "piece images are loaded in main()"
                screen.blit(square.piece.image, (square.y * SQUARE_SIZE + (SQUARE_SIZE - square.piece.width) / 2, square.x * SQUARE_SIZE + (SQUARE_SIZE - square.piece.height) / 2))       

    # Outline the selected piece's square
    if selectedSquare is not None:
        rect = pygame.Rect(selectedSquare.y * SQUARE_SIZE, selectedSquare.x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, HIGHLIGHT_COLOUR, rect, HIGHLIGHT_WIDTH)

    # Dim the board and show a banner, e.g. "CHECKMATE"
    if message is not None:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOUR)
        screen.blit(overlay, (0, 0))
        text = bannerFont().render(message, True, BANNER_COLOUR)
        screen.blit(text, text.get_rect(center=screen.get_rect().center))

@functools.cache
def bannerFont():
    return pygame.font.Font(None, 140)

if __name__ == "__main__":
    main()