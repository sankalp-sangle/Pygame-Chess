# Import the pygame module
import pygame

from chessBoard import ChessBoard

def updatePosition(chessBoard):
    if addX:
        chessBoard.x += 1
    else:
        chessBoard.x -= 1
    if addY:
        chessBoard.y += 1
    else:
        chessBoard.y -= 1

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Sankalp Chess")
icon = pygame.image.load('../img/chess.png')
pygame.display.set_icon(icon)

addX = True
addY = True

state_running = True

chessBoard = ChessBoard(0, 0, '../img/chessboard.png')
chessBoard.image = pygame.image.load(chessBoard.image_path)

while state_running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            state_running = False

    screen.fill((70,0,40))
    screen.blit(chessBoard.image, (chessBoard.x, chessBoard.y))
    updatePosition(chessBoard)

    if chessBoard.x == 500 or chessBoard.x == 0:
        addX = not addX
    if chessBoard.y == 300 or chessBoard.y == 0:
        addY = not addY

    pygame.display.update()