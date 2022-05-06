"""
Player module
"""


import random
from copy import deepcopy

import pygame
from checkers.cons import GREEN, SQUARE_SIZE, ROWS, WHITE, BLACK

class humanPlayer:
    def __init__(self,color):
        self.color = color
        self.selected = None
        self.valid_moves=[]

    def get_row_col_from_mouse(self,pos):
        x, y = pos
        print(x, y)
        row = y // SQUARE_SIZE + 1
        col = x // SQUARE_SIZE + 1
        board_num = 1
        if col > ROWS + 1:
            col = col - ROWS - 2
            board_num = 2
        return row, col, board_num

    def is_valid_move(self,row,col,board_num):
        for move in self.valid_moves:
            for i in range(len(move)):
                if board_num==move[i]['end_board']:
                    if [row,col]==move[i]['end_move']:
                        return move[i]
        return False

    def select(self, row, col, board_num, gameState):
        if self.selected:
            next_move = self.is_valid_move(row, col, board_num)
            self.selected = None
            if next_move:
                return next_move
            else:
                return False

        board=gameState.boards.board1 if board_num==1 else gameState.board2
        piece = board[row][col]
        if piece != 0 and piece != 1 and piece.color == self.gs.player:
            self.selected = piece
            one_moves,two_moves,transfer_moves = gameState.get_valid_moves_piece(piece,board,board_num)
            self.valid_moves=one_moves+two_moves+transfer_moves
            return False
        return False


class randomPlayer:
    def __init__(self, color):
        self.player_tag = 'Random'
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
        self.player_tag = 'Minimax_{}[{}]'.format(strategy, depth)
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
            node_score = self.minimax_moves(player,gamestate=next_gamestate, max_player=True, depth=self.depth)
            if node_score >= highest_score:
                highest_score = node_score
                best_move = next_move

        return best_move


    def minimax_moves(self, player,gamestate, max_player, depth):
        """
        Minimax pseudocode was referred from:
        https://www.youtube.com/watch?v=l-hh51ncgDI&t=254s
        """
        print("depth", depth)
        gamestate.reset()
        next_move_options = gamestate.get_all_valid_moves()
        gamestate.player = WHITE if gamestate.player == BLACK else BLACK
        gamestate.opponent = WHITE if gamestate.opponent == BLACK else BLACK
        if depth == 0 or game_over(gamestate):
            return gamestate.evaluation(strategy=self.strategy)
        if max_player:
            max_value = float('-inf')
            # loop each child
            for next_move_info in next_move_options:
                # generate new gamestate
                next_gamestate = simulate_move(gamestate, next_move_info,player)
                # evaluation
                value = self.minimax_moves(player,gamestate=next_gamestate, max_player=False, depth=depth - 1)

                max_value = max(max_value, value)
            print("max_value",max_value)
            return max_value
        else:
            print("min_player")
            min_value = float('inf')
            for next_move_info in next_move_options:
                print("next_move_info:",next_move_info)

                next_gamestate = simulate_move(gamestate, next_move_info,player)

                value = self.minimax_moves(player,gamestate=next_gamestate, max_player=True, depth=depth - 1)
                min_value = min(min_value, value)
            print("min_value",min_value)
            return min_value


def game_over(game):
    all_moves = game.get_all_valid_moves()
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


def simulate_move(game, next_move,player):
    simulated_game = deepcopy(game)
    for move in next_move:
        simulated_game.boards.draw_board(player.win)
        if move['start_board'] == 1:
            piece = simulated_game.boards.board1[move['start_move'][0]][move['start_move'][1]]
            if piece!=0:
                one_moves, two_moves, transfer_moves = simulated_game.get_valid_moves_piece(piece, simulated_game.boards.board1,1)
        else:
            piece = simulated_game.boards.board2[move['start_move'][0]][move['start_move'][1]]
            if piece != 0:
                one_moves, two_moves, transfer_moves = simulated_game.get_valid_moves_piece(piece, simulated_game.boards.board2,2)
        if piece!=0:
            one_move_list = [[m] for m in one_moves]
            valid_moves = one_move_list + two_moves + transfer_moves
            pygame.draw.circle(player.win, (0, 255, 0), (piece.x, piece.y), 30, 5)

            player.draw_valid_moves(valid_moves)
            pygame.display.update()
            pygame.time.delay(200)
        if move['start_board'] != move['end_board']:
            simulated_game.transfer_piece(move, make_move=True)
        else:
            if move['start_board'] == 1:
                simulated_game.update_board_normal(move, simulated_game.boards.board1, make_move=True)
            else:
                simulated_game.update_board_normal(move, simulated_game.boards.board2, make_move=True)

    return simulated_game








    # pygame.time.delay(100)
