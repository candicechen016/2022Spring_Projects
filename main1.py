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

import numpy as np
import random


class GameState:
    def __init__(self, board_size, player,board1, board2):
        self.board1 = board1
        self.board2 = board2
        self.board_size = board_size
        self.player=player
        self.opponent='b' if self.player=='w' else 'w'

        self.w_position = self.get_positions('w')
        self.b_position = self.get_positions('b')

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
        two_move_list = []
        for position in positions:
            if board1[position[0] - 1, position[1] + 1] == '.':
                next_one_move=self.move(self.player + '1', position, [position[0] - 1, position[1] + 1], board, False)
                one_move_list.append(next_one_move)
                if board1[position[0] - 1, position[1] + 1][0] == self.opponent and board1[position[0] - 2, position[1] + 2][0]=='.':
                    next_two_move=self.move(self.player + '1', position, [position[0] - 2, position[1] + 2], board, True)
            if board1[position[0] + 1, position[1] + 1] == '.':
                one_move_list.append(self.move(self.player + '1', position, [position[0] + 1, position[1] + 1], board, False))
        return one_move_list



    def movie_list(self):
        """
        :param positions1: postions of pieces in original board, ex. w1 in board1, b2 in board2
        :param king_postions1: postions of king pieces in original board, ex. w1k in board1, b2k in board2
        :param postions2: postions of pieces in tranfer board, ex. w2 in board1, b1 in board2
        :param king_positions: postions of king pieces in tranfer board, ex. w2k in board1, b1k in board2
        :param board:  original board for current player
        :param tranfer_board: transfer board for current player
        :return:
        """
        pass

    def update_board(self, player, position, next_position, board, capture):
        board[position[0], position[1]] = '.'
        board[next_position[0], next_position[1]] = player  # change to king
        if capture:
            board[position[0], position[1]] = '.'
            board[next_position[0], next_position[1]] = player
            board[(position[0] + next_position[0]) / 2, (position[1] + next_position[1]) / 2] = '.'
        return board


if __name__ == '__main__':
    board1 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, 'w1', '.', 'w1', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', 'b1', '.', 'b1', 1],
                       [1, 1, 1, 1, 1, 1]])

    board2 = np.array([[1, 1, 1, 1, 1, 1],
                       [1,'.', 'w2', '.', 'w2',1],
                       [1,'.', '.', '.', '.',1],
                       [1,'.', '.', '.', '.',1],
                       [1,'b2', '.', 'b2', '.',1],
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

    gs1 = GameState(4,'w',board1, board2)

    print(gs1.w_position)
    print(gs1.opponent)
