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
    def __init__(self, window):
        self.gs = GameState(BLACK, Boards(), 0)
        self.turn_num = 0
        self.window = window
        self.valid_moves = []
        self.selected = None

    def draw_valid_moves(self, moves):
        for move in moves:
            for i in range(len(move)):
                if move[i]['end_board'] == 1:
                    row, col = move[i]['end_move'][0] - 1, move[i]['end_move'][1] - 1
                    pygame.draw.circle(self.window, GREEN,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
                if move[i]['end_board'] == 2:
                    row, col = move[i]['end_move'][0] - 1, move[i]['end_move'][1] + ROWS + 1
                    pygame.draw.circle(self.window, GREEN,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

    def update_window(self):
        self.gs.boards.draw_board(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def human_move(self, next_move):
        self.update_board(next_move)
        self.turn_num += 1
        if self.turn_num % 2 == 0:
            self.change_turn()


    def computer_move(self, next_moves):
        for move in next_moves:
            self.update_board(move)
        self.turn_num += 2
        self.change_turn()

    def change_turn(self):
        self.valid_moves = []
        if self.gs.player == BLACK:
            self.gs.player = WHITE
            self.gs.opponent = BLACK
        else:
            self.gs.player = BLACK
            self.gs.opponent = WHITE

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE + 1
        col = x // SQUARE_SIZE + 1
        board_num = 1
        if col > ROWS + 1:
            col = col - ROWS - 2
            board_num = 2
        return row, col, board_num

    def select(self, row, col, board_num):
        if self.selected:
            result = self.human_move(row, col, board_num)
            if not result:
                self.selected = None
                self.select(row, col, board_num)
        board = self.gs.boards.board1 if board_num == 1 else self.gs.boards.board2
        piece = board[row][col]
        if piece != 0 and piece and piece.color == self.gs.player:
            self.selected = piece
            one_moves, two_moves, transfer_moves = self.gs.get_valid_moves_piece(piece)
            self.valid_moves = one_moves[1] + one_moves[2] + two_moves + transfer_moves
            return True
        return False

    def is_valid_move(self, row, col, board_num):
        for move in self.valid_moves:
            if board_num == move[0]['end_board']:
                if (row, col) == move[0]['end_move']:
                    return move[0]
        return False

    def human_move(self, row, col, board_num):
        move = self.is_valid_move(row, col, board_num)
        if self.selected and move:
            self.update_board(move)
            self.turn_num += 1
            if self.turn_num % 2 == 0:
                self.change_turn()
        else:
            return False
        return True

    def update_board(self, next_move):
        if next_move['start_board'] != next_move['end_board']:
            self.gs.transfer_piece(next_move, make_move=True)
        else:
            if next_move['start_board'] == 1:
                self.gs.update_board_normal(next_move, self.gs.boards.board1, make_move=True)
            else:
                self.gs.update_board_normal(next_move, self.gs.boards.board2, make_move=True)
        self.gs.reset()
