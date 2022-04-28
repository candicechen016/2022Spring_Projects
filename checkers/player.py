import random

import pygame

from checkers.cons import GREEN, SQUARE_SIZE, ROWS, WHITE, BLACK
from checkers.gameState import GameState


class randomPlayer:
    def __init__(self,color):
        self.win_count = 0
        self.color=color

    def get_next_move(self, next_move_options):
        mode1_num = len(next_move_options['one_move'])
        mode2_num = len(next_move_options['two_move'])
        mode3_num = len(next_move_options['transfer_move'])
        option_list = [1] * mode1_num + [2] * mode2_num + [3] * mode3_num
        next_move = []
        next_move_mode=0
        if option_list:
            next_move_mode = random.choice(option_list)
            if next_move_mode == 1:
                next_move = random.choice(next_move_options['one_move'])
            elif next_move_mode == 2:
                next_move = random.choice(next_move_options['two_move'])
            elif next_move_mode == 3:
                next_move = random.choice(next_move_options['transfer_move'])
        return next_move,next_move_mode

class MinimaxPlayer:

    def __init__(self, piece, ai=False, strategy=0):
        self.piece = piece
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0

    def minimax_moves(self, next_move_options):
        pass


#refer
class Board:
    pass


class humanPlayer:
    def __init__(self,win,gs):
        self.win=win
        self.gs=gs

    def reset(self):
        self.selected = None
        self.turn = WHITE
        self.valid_moves = {}

    def draw_valid_moves(self,moves):
        for move in moves:
            for i in range(2):
                if move['end_board']=='board1':
                    row,col=move[i]['end_move'][i],move[i]['end_move'][1]
                else:
                    row, col = move[i]['end_move'][i], move[i]['end_move'][1]+ROWS+1
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    #refer
    def update_win(self):
        self.boards.draw_board(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col,board_num):
        if self.selected:
            result = self._move(row, col,board_num)
            if not result:
                self.selected = None
                self.select(row, col,board_num)

        board=self.gs.board1 if board_num==1 else self.gs.board2
        piece = board[row][col]
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.gs.get_valid_moves_piece(piece)
            return True
        return False

    def get_move(self,row,col,board_num):
        for move in self.valid_moves:
            for i in range(len(move)):
                if board_num==move[i]['end_board']:
                    if [row,col]==move[i]['end_move'] or [row,col] in move[i]['capture']:
                        return move[i]
        return False

    def _move(self, row, col,board_num):
        board = self.gs.board1 if board_num == 1 else self.gs.board2
        piece = board[row][col]
        move=self.get_move(row,col,board_num)
        if self.selected and piece == 0 and move:
            if move['start_board']==move['end_board']:
                self.gs.update_board_normal(move, board, True)
            else:
                self.gs.transfer_piece(move, make_move=True)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK