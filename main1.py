"""
Parallel-Universes Checkers.

winninig:
1. NO PIECES on both boards
2. NO STEPS AND NO TRANFE on both boards
rules:
1. can only Transfer once
2. can not capture at the transferring round
3. only transfer to an empty square and must go to an orthogonally-adjacent square
4. Make Moves:
    a. move one piece at the same universe two turns
    b. move one piece of each board

"""
import copy

import numpy as np
import random


class GameState:
    def __init__(self, board_size, player, board1, board2):
        self.board1 = board1
        self.board2 = board2
        self.board_size = board_size
        self.player = player
        self.direction = 1 if self.player == 'w' else -1
        self.opponent = 'b' if self.player == 'w' else 'w'

        self.positions = self.get_positions(self.player)
        self.opponent_position = self.get_positions(self.opponent)

    def get_positions(self, player):
        return {'board1': {'positions1': np.argwhere(self.board1 == player + '1'),
                           'king_positions1': np.argwhere(self.board1 == player + '1k'),
                           'positions2': np.argwhere(self.board1 == player + '2'),
                           'king_positions2': np.argwhere(self.board1 == player + '2k')
                           },
                'board2': {'positions1': np.argwhere(self.board2 == player + '1'),
                           'king_positions1': np.argwhere(self.board2 == player + '1k'),
                           'positions2': np.argwhere(self.board2 == player + '2'),
                           'king_positions2': np.argwhere(self.board2 == player + '2k')}}

    def get_normal_move(self, positions, board):

        one_move_list = []
        for position in positions:
            next_row = position[0] + self.direction
            next_col_list = [position[1] - 1, position[1] + 1]
            for next_col in next_col_list:
                if board[next_row, next_col] == '.':
                    next_one_move = self.update_board(self.player + '1', position, [next_row, next_col], board, False)
                    one_move_list.append(next_one_move)
                    for i in [1, -1]:
                        if board[next_row, next_col][0] == self.opponent and board[next_row + self.direction, next_col + i] == '.':
                            next_capture_move = self.update_board(self.player + '1', position, [next_row + self.direction, next_col + i],
                                                                  board, True)
                            one_move_list.append(next_capture_move)
        return one_move_list

    def move_list(self):
        """
        :param positions1: postions of pieces in original board, ex. w1 in board1, b2 in board2
        :param king_postions1: postions of king pieces in original board, ex. w1k in board1, b2k in board2
        :param postions2: postions of pieces in tranfer board, ex. w2 in board1, b1 in board2
        :param king_positions: postions of king pieces in tranfer board, ex. w2k in board1, b1k in board2
        :param board:  original board for current player
        :param tranfer_board: transfer board for current player
        :return:
        """
        one_move_list = {'board1': self.get_normal_move(self.positions['board1']['positions1'], self.board1),
                         'board2': self.get_normal_move(self.positions['board1']['positions2'], self.board2)}

        return one_move_list

    def update_board(self, player, position, next_position, board, capture):
        board_temp=copy.deepcopy(board)
        board_temp[position[0], position[1]] = '.'
        board_temp[next_position[0], next_position[1]] = player  # change to king
        if capture:
            board_temp[position[0], position[1]] = '.'
            board_temp[next_position[0], next_position[1]] = player
            board_temp[(position[0] + next_position[0]) / 2, (position[1] + next_position[1]) / 2] = '.'
        return board_temp


if __name__ == '__main__':
    board1 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, 'w1', '.', 'w1', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', 'b1', '.', 'b1', 1],
                       [1, 1, 1, 1, 1, 1]])

    board2 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, '.', 'w2', '.', 'w2', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, 'b2', '.', 'b2', '.', 1],
                       [1, 1, 1, 1, 1, 1]])
    #
    # board1 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
    #                    [1, 'w1', '.', 'w1', '.', 'w1', '.', 1],
    #                    [1, '.', 'w1', '.', 'w1', '.', 'w1', 1],
    #                    [1, '.', '.', '.', '.', '.', '.', 1],
    #                    [1, '.', '.', '.', '.', '.', '.', 1],
    #                    [1, 'b1', '.', 'b1', '.', 'b1', '.', 1],
    #                    [1, '.', 'b1', '.', 'b1', '.', 'b1', 1],
    #                    [1, 1, 1, 1, 1, 1, 1, 1]])
    #
    # board2 = np.array([
    #     [1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, '.', 'w2', '.', 'w2', '.', 'w2', 1],
    #     [1, 'w2', '.', 'w2', '.', 'w2', '.', 1],
    #     [1, '.', '.', '.', '.', '.', '.', 1],
    #     [1, '.', '.', '.', '.', '.', '.', 1],
    #     [1, '.', 'b2', '.', 'b2', '.', 'b2', 1],
    #     [1, 'b2', '.', 'b2', '.', 'b2', '.', 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1]])

    gs1 = GameState(4, 'w', board1, board2)

    print(gs1.move_list())
