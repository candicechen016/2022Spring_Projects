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
from copy import deepcopy
import random


class GameState:
    def __init__(self):
        board1 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 'w1', '.', 'w1', '.', 'w1', '.', 1],
                                [1, '.', 'w1', '.', 'w1', '.', 'w1', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, 'b1', '.', 'b1', '.', 'b1', '.', 1],
                                [1, '.', 'b1', '.', 'b1', '.', 'b1', 1],
                                [1, 1, 1, 1, 1, 1, 1, 1]])

        board2 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                [1, '.', 'w2', '.', 'w2', '.', 'w2', 1],
                                [1, 'w2', '.', 'w2', '.', 'w2', '.', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, '.', 'b2', '.', 'b2', '.', 'b2', 1],
                                [1, 'b2', '.', 'b2', '.', 'b2', '.', 1],
                                [1, 1, 1, 1, 1, 1, 1, 1]])

        self.boards = {'1': board1, '2': board2}

    def find_orthogonally_neighbors(self, piece_position, board):
        x, y = piece_position
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        empty = []
        for n in neighbors:
            if board[n] == '.':
                empty.append(n)
        return empty

    def check_win(self, player):

        all_valid = []
        for board in self.boards.values():
            for piece in player:
                piece_positions = np.argwhere(board == piece)
                # condition 1: the player has NO PIECES on Both boards
                if piece_positions.size == 0:
                    continue
                else:
                    # condition 2: the player has NO STEPS AND NO way to transfer on both boards

                    for position in piece_positions:
                        valid_transfer_squares = self.find_orthogonally_neighbors(piece, position, board)
                        all_valid += valid_transfer_squares
        if not all_valid:
            return True
        # else:
        #     for position in valid_transfer_squares:
        #         # TODO: call make move function and get the boards
        else:
            return False

    def transfer_piece(self, player, position, next_position, board1, board2):
        new_board1 = deepcopy(board1)
        new_board2 = deepcopy(board2)
        new_board1[position[0], position[1]] = '.'
        new_board2[next_position[0], next_position[1]] = player  # change to king
        return (new_board1, new_board2)

    def get_transferred_list(self, player):
        if player[1] == '1':
            board1 = self.boards['1']
            board2 = self.boards['2']
        else:
            board1 = self.boards['2']
            board2 = self.boards['1']

        positions_current_board = np.argwhere(board1 == player)
        transfer_move_list = []
        for piece in positions_current_board:
            list = self.find_orthogonally_neighbors(piece, board2)

            if list:
                for move in list:
                    next_move = self.transfer_piece(player, piece, move, board1, board2)
                    transfer_move_list.append(next_move)
        return transfer_move_list











if __name__ == '__main__':
    game = GameState()

    print(game.boards['1'])
    print(game.boards['2'])