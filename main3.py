"""
UI reference: https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
"""

import pygame

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 8, 18
SQUARE_SIZE = HEIGHT//ROWS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GOLD=(255,215,0)
SILVER=(192,192,192)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (20, 10))

WIN= pygame.display.set_mode((WIDTH*2+2*SQUARE_SIZE, HEIGHT))
FPS=60

class Boards:
    def __init__(self):
        self.board1=[]
        self.board2=[]
        self.create_board()

    def draw_grids(self,win):
        win.fill(BLUE)
        pygame.draw.line(win,RED,[ROWS*SQUARE_SIZE,0],[ROWS*SQUARE_SIZE,ROWS*SQUARE_SIZE],5)
        pygame.draw.line(win, RED, [(ROWS+2) * SQUARE_SIZE, 0], [(ROWS+2) * SQUARE_SIZE, ROWS * SQUARE_SIZE], 5)
        for col in range(ROWS):
            for row in range(col%2, ROWS, 2):
                pygame.draw.rect(win,RED,(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
                pygame.draw.rect(win, RED, ((col+ROWS+2) * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        self.board1.append([1] * (ROWS + 2))
        self.board2.append([1] * (ROWS + 2))
        for row in range(1,ROWS+1):
            self.board1.append([1])
            self.board2.append([1])
            for col in range(1,ROWS+1):
                if col%2==(row%2):
                    if row<4:
                        self.board1[row].append(Piece(row,col,WHITE,1))
                    elif row>5:
                        self.board1[row].append(Piece(row,col,BLACK,1))
                    else:
                        self.board1[row].append(0)
                else:
                    self.board1[row].append(0)
                if col % 2 == ((row+1) % 2):
                    if row<4:
                        self.board2[row].append(Piece(row,col+ROWS+2,WHITE,2))
                    elif row>5:
                        self.board2[row].append(Piece(row,col+ROWS+2,BLACK,2))
                    else:
                        self.board2[row].append(0)
                else:
                    self.board2[row].append(0)
            self.board1[row].append(1)
            self.board2[row].append(1)
        self.board1.append([1] * (ROWS + 2))
        self.board2.append([1] * (ROWS + 2))

    def draw_board(self,win):
        self.draw_grids(win)
        print(self.board1)
        print(self.board2)
        for row in range(1,ROWS+1):
            for col in range(1,ROWS+1):
                piece1 = self.board1[row][col]
                piece2 = self.board2[row][col]
                if piece1 !=0:
                    piece1.draw(win)
                if piece2 !=0:
                    piece2.draw(win)



class Piece:
    PADDING = 11
    OUTLINE = 3

    def __init__(self, row, col, color,board_num):
        self.board_num=board_num
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.direction=[-1] if self.color==BLACK else [1]
        if self.king:
            self.direction = [-1, 1]

    def calc_pos(self):
        self.x = SQUARE_SIZE * (self.col-1) + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * (self.row-1)+ SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        if self.board_num==1:
            pygame.draw.circle(win, GOLD, (self.x, self.y), radius + self.OUTLINE)
        else:
            pygame.draw.circle(win, SILVER, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)



# def main():
#     run=True
#     boards=Boards()
#
#     clock = pygame.time.Clock()
# #
#     while run:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#              if event.type==pygame.QUIT:
#                  run=False
#         boards.draw_board(WIN)
#         pygame.display.update()
#     pygame.quit()
# main()