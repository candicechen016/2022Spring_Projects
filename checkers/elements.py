#refer
import pygame

from checkers.cons import BLUE, RED, ROWS, SQUARE_SIZE, WHITE, BLACK, GOLD, SILVER, CROWN


class Boards:
    def __init__(self):
        self.board1=[]
        self.board2=[]
        self.w_left = self.b_left = (ROWS//2-1)*ROWS//2
        self.w_king_left = self.b_king_left = 0
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
                    if row<ROWS//2:
                        self.board1[row].append(Piece(row,col,WHITE,1,GOLD))
                    elif row>ROWS//2+1:
                        self.board1[row].append(Piece(row,col,BLACK,1,GOLD))
                    else:
                        self.board1[row].append(0)
                else:
                    self.board1[row].append(0)
                if col % 2 == ((row+1) % 2):
                    if row<ROWS//2:
                        self.board2[row].append(Piece(row,col,WHITE,2,SILVER))
                    elif row>ROWS//2+1:
                        self.board2[row].append(Piece(row,col,BLACK,2,SILVER))
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

    def __init__(self, row, col, color,board_num,coat):
        self.board_num=board_num
        self.row = row
        self.col = col
        self.color = color
        self.sign='w' if self.color==WHITE else 'b'
        self.king = False
        self.coat=coat
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.direction=(-1) if self.color==BLACK else (1)

    def calc_pos(self):
        self.y = SQUARE_SIZE * (self.row - 1) + SQUARE_SIZE // 2
        if self.board_num==1:
            self.x = SQUARE_SIZE * (self.col-1) + SQUARE_SIZE // 2
        else:
            self.x = SQUARE_SIZE * (self.col+ROWS+1) + SQUARE_SIZE // 2


    def make_king(self):
        self.king = True
        self.direction = (-1, 1)

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self.coat, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.sign)+str(self.board_num)+str(self.king)
