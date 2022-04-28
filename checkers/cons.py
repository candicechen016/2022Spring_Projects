import pygame

WIDTH, HEIGHT = 400, 400
# ROWS, COLS = 8, 18
ROWS=4
COLS = 2*ROWS+2
SQUARE_SIZE = HEIGHT//ROWS


RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GOLD=(255,215,0)
SILVER=(192,192,192)
YELLOW=(0,128,128)
GREEN=(0, 255, 0)

CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (20, 10))


