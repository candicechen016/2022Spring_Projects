import random
from copy import deepcopy

import pygame
from numpy.ma import copy

from checkers.cons import GREEN, SQUARE_SIZE, ROWS, WHITE, BLACK
from checkers.elements import Boards
from checkers.gameState import GameState


class randomPlayer:
    def __init__(self, color):
        self.plyer_tag = 'random'
        self.win_count = 0
        self.color = color

    def get_next_move(self, gamestate):
        next_move_options = gamestate.get_valid_moves()
        mode1_num = len(next_move_options['one_move'])
        mode2_num = len(next_move_options['two_move'])
        mode3_num = len(next_move_options['transfer_move'])
        option_list = [1] * mode1_num + [2] * mode2_num + [3] * mode3_num
        next_move = []
        # next_move_mode = 0
        if option_list:
            next_move_mode = random.choice(option_list)
            if next_move_mode == 1:
                next_move = random.choice(next_move_options['one_move'])
            elif next_move_mode == 2:
                next_move = random.choice(next_move_options['two_move'])
            elif next_move_mode == 3:
                next_move = random.choice(next_move_options['transfer_move'])
        return next_move


class MinimaxPlayer:

    def __init__(self, piece, strategy, depth):
        self.plyer_tag = 'ai'
        self.color = piece
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0
        self.strategy = strategy  # 'kings' or 'capture'
        self.depth = depth

    def get_next_move(self, gamestate):
        next_move_options = gamestate.get_all_valid_moves()
        best_move = None
        highest_score = 0

        for idx, next_move in enumerate(next_move_options):
            next_gamestate = simulate_move(gamestate, next_move)
            node_score = self.minimax_moves(gamestate=next_gamestate, max_player=True, depth=self.depth)
            if node_score >= highest_score:
                highest_score = node_score
                best_move = next_move

        return best_move


    def minimax_moves(self, gamestate, max_player, depth):
        """
        Minimax pseudocode was referred from:
        https://www.youtube.com/watch?v=l-hh51ncgDI&t=254s
        """
        print("depth", depth)
        gamestate.reset()
        next_move_options = gamestate.get_all_valid_moves()

        if depth == 0 or game_over(gamestate):
            return gamestate.evaluation(strategy=self.strategy)
        if max_player:
            max_value = float('-inf')
            # loop each child
            for next_move_info in next_move_options:
                # generate new gamestate
                next_gamestate = simulate_move(gamestate, next_move_info)
                # evaluation
                value = self.minimax_moves(gamestate=next_gamestate, max_player=False, depth=depth - 1)

                max_value = max(max_value, value)
            print("max_value",max_value)
            return max_value
        else:
            print("min_player")
            min_value = float('inf')
            for next_move_info in next_move_options:
                print("next_move_info:",next_move_info)
                next_gamestate = simulate_move(gamestate, next_move_info)

                value = self.minimax_moves(gamestate=next_gamestate, max_player=True, depth=depth - 1)
                min_value = min(min_value, value)
            print("min_value",min_value)
            return min_value


def game_over(game):
    all_moves = game.get_all_valid_moves
    has_pieces = 0
    # condition 1: the player has NO STEPS and NO WAY to transfer to both boards
    if not all_moves:
        print('no_moves:', game.opponent, 'wins')
        return True
    for board_name in ['board1', 'board2']:
        # condition 2: the player has NO PIECES on Both boards
        if len(game.positions[board_name]) == 0:
            has_pieces += 1
            continue
    if has_pieces == 2:
        print('No piece:', game.opponent, 'wins')
        return True
    # draw: no capture in 50 turns
    if game.no_capture >= 50:
        print('draw')
        return True


def simulate_move(game, next_move):
    simulated_game = deepcopy(game)
    for move in next_move:
        if move['start_board'] != move['end_board']:
            simulated_game.transfer_piece(move, make_move=True)
        else:
            if move['start_board'] == 1:
                simulated_game.update_board_normal(move, simulated_game.boards.board1, make_move=True)
            else:
                simulated_game.update_board_normal(move, simulated_game.boards.board2, make_move=True)

    return simulated_game


#refer

class humanPlayer:
    def __init__(self,win,gs):
        self.win=win
        self.gs=gs
        self.selected = None
        self.turn = WHITE
        self.valid_moves=[]
        self.selected = None


    def draw_valid_moves(self,moves):
        for move in moves:
            for i in range(len(move)):
                if move[i]['end_board']==1:
                    row,col=move[i]['end_move'][0]-1,move[i]['end_move'][1]-1
                    pygame.draw.circle(self.win, GREEN,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
                if move[i]['end_board'] == 2:
                    row, col = move[i]['end_move'][0]-1, move[i]['end_move'][1]+ROWS+1
                    pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)

    #refer
    def update_win(self):
        self.gs.boards.draw_board(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col,board_num):
        if self.selected:
            result = self._move(row, col,board_num)
            if not result:
                self.selected = None
                self.select(row, col,board_num)

        board=self.gs.boards.board1 if board_num==1 else self.gs.boards.board2
        piece = board[row][col]
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            one_moves,two_moves,transfer_moves = self.gs.get_valid_moves_piece(piece,board,board_num)
            one_move_list=[[m] for m in one_moves]
            self.valid_moves=one_move_list+two_moves+transfer_moves
            for i in self.valid_moves:
                print(i)
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
        board = self.gs.boards.board1 if board_num == 1 else self.gs.boards.board2
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