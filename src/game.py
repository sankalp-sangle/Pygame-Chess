# Import the pygame module
import pygame

from infra import ChessBoard, Square
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn

SQUARE_SIZE   = 100
NO_OF_SQUARES = 8

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

    for row in range(len(board.squares)):
        for col in range(len(board.squares[0])):
            square = board.squares[row][col]
            square.image = pygame.image.load(square.image_path)
            if square.piece:
                square.piece.image = pygame.image.load(square.piece.image_path)
            
    isWhiteTurn = True

    state_running = True

    isPieceSelected = False
    selectedPiece = None

    while state_running:
        printBoard(screen, board)       

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if not isPieceSelected:                    
                    if board.squares[row][col].piece:
                        isPieceSelected = True
                        selectedPiece = board.squares[row][col].piece
                else:
                    decision = (isWhiteTurn == selectedPiece.isWhite) and selectedPiece.validate(row, col, board)
                    if decision:
                        oldSquare = selectedPiece.square
                        pieceOnNewSquare = board.squares[row][col].piece
                        wasOccupied = board.squares[row][col].isOccupied

                        # Assign new position to piece
                        selectedPiece.x = row
                        selectedPiece.y = col
                        
                        # Remove piece for earlier square
                        selectedPiece.square.piece = None
                        selectedPiece.square.isOccupied = False

                        # Assign piece to new square and new square to piece
                        selectedPiece.square = board.squares[row][col]
                        board.squares[row][col].piece = selectedPiece
                        board.squares[row][col].isOccupied = True

                        # Check if new position leaves the king in check
                        if kingUnderCheck(board, whiteKing if isWhiteTurn else blackKing):
                            # Revert the changes
                            selectedPiece.square.piece = pieceOnNewSquare
                            oldSquare.piece = selectedPiece
                            selectedPiece.square.isOccupied = wasOccupied
                            selectedPiece.x, selectedPiece.y = oldSquare.x, oldSquare.y
                            selectedPiece.square = oldSquare
                            oldSquare.isOccupied = True
                            board.consideringEnPassant = False
                        else:
                            # Check for pawn promotion
                            if isinstance(selectedPiece, Pawn) and ((selectedPiece.isWhite and selectedPiece.x == 0) or (not selectedPiece.isWhite and selectedPiece.x == 7)):
                                selectedPiece.square.piece = Queen(x = selectedPiece.x, y = selectedPiece.y, path = '../img/' + ('white' if selectedPiece.isWhite else 'black') + '/queen.png', square = selectedPiece.square, isWhite = selectedPiece.isWhite)
                                selectedPiece = selectedPiece.square.piece
                                selectedPiece.image = pygame.image.load(selectedPiece.image_path)

                            # After successful move, flip turn variable
                            isWhiteTurn = not isWhiteTurn

                            # If an En Passant move, remove the captured pawn
                            if board.consideringEnPassant:
                                board.lastPieceMoved.square.piece = None
                                board.lastPieceMoved.square.isOccupied = False
                                board.consideringEnPassant = False

                            # Update last piece moved
                            board.lastPieceMoved = selectedPiece

                    # Remove selected piece
                    isPieceSelected = False
                    selectedPiece = None
                    
        pygame.display.update()

def printBoard(screen, board):
    for row in range(len(board.squares)):
        for col in range(len(board.squares[0])):
            square = board.squares[row][col]
            screen.blit(square.image, (square.y * SQUARE_SIZE, square.x * SQUARE_SIZE))       
            if square.piece:
                screen.blit(square.piece.image, (square.y * SQUARE_SIZE + (SQUARE_SIZE - square.piece.width) / 2, square.x * SQUARE_SIZE + (SQUARE_SIZE - square.piece.height) / 2))       

if __name__ == "__main__":
    main()