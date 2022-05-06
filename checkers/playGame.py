"""

Reference:
Our structure of the playGame class mainly referred to this source:
https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/game.py

"""
import pygame

from checkers.cons import GREEN, SQUARE_SIZE, ROWS, BLACK, WHITE
from checkers.elements import Boards
from checkers.gameState import GameState


class playGame:
    def __init__(self,window):
        self.win=window
        self.gs=GameState(WHITE, Boards(), 0)
        self.turn_num=0


    def draw_valid_moves(self,moves):
        for move in moves:
            for i in range(len(move)):
                if move[i]['end_board']==1:
                    row,col=move[i]['end_move'][0]-1,move[i]['end_move'][1]-1
                    pygame.draw.circle(self.win, GREEN,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
                if move[i]['end_board'] == 2:
                    row, col = move[i]['end_move'][0]-1, move[i]['end_move'][1]+ROWS+1
                    pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)

    def update_window(self,valid_moves=[]):
        self.gs.boards.draw_board(self.win)
        self.draw_valid_moves(valid_moves)
        pygame.display.update()

    def human_move(self, next_move):

        self.update_board(next_move)
        self.turn_num += 1
        if self.turn_num % 2 == 0:
            self.change_turn()

    def update_board(self,next_move):
        if next_move['start_board'] != next_move['end_board']:
            self.gs.transfer_piece(next_move, make_move=True)
        else:
            if next_move['start_board'] == 1:
                self.gs.update_board_normal(next_move, self.gs.boards.board1, make_move=True)
            else:
                self.gs.update_board_normal(next_move, self.gs.boards.board2, make_move=True)
        self.gs.reset()

    def change_turn(self):
        if self.gs.player == BLACK:
            self.gs.player = WHITE
            self.gs.opponent=BLACK
        else:
            self.gs.player = BLACK
            self.gs.opponent = WHITE

    def computer_move(self, next_moves):
        for move in next_moves:
            self.update_board(move)
        self.turn_num+=2
        self.change_turn()