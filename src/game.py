# Import the pygame module
import pygame

from chessBoard import ChessBoard
from pieces import Queen

# Initialize pygame
pygame.init()

directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

def updatePosition(queen, key):
    if key == pygame.K_UP:
        queen.y = max(202, queen.y - 37.5)
    if key == pygame.K_DOWN:
        queen.y = min(502 - 37.5, queen.y + 37.5)
    if key == pygame.K_LEFT:
        queen.x = max(302, queen.x - 37.5)
    if key == pygame.K_RIGHT:
        queen.x = min(602 - 37.5, queen.x + 37.5)

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Sankalp Chess")
icon = pygame.image.load('../img/chess.png')
pygame.display.set_icon(icon)

addX = True
addY = True

state_running = True

chessBoard = ChessBoard(300, 200, '../img/chessboard.png')
chessBoard.image = pygame.image.load(chessBoard.image_path)

queen = Queen(302,202,'../img/queen.png')
queen.image = pygame.image.load(queen.image_path)


screen.fill((70,0,40))




while state_running:
    screen.blit(chessBoard.image, (chessBoard.x, chessBoard.y))
    screen.blit(queen.image, (queen.x, queen.y))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            state_running = False
        if event.type == pygame.KEYDOWN:
            if event.key in directions:
                updatePosition(queen, event.key)
    

    pygame.display.update()