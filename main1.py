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
        """
          :param positions1: postions of pieces in original board, ex. w1 in board1, b2 in board2
          :param king_postions1: postions of king pieces in original board, ex. w1k in board1, b2k in board2
          :param postions2: postions of pieces in tranfer board, ex. w2 in board1, b1 in board2
          :param king_positions: postions of king pieces in tranfer board, ex. w2k in board1, b1k in board2
          :param board:  original board for current player
          :param tranfer_board: transfer board for current player
          :return:
          """
        return {'board1': {'positions1': np.argwhere(self.board1 == player + '1'),
                           'king_positions1': np.argwhere(self.board1 == player + '1k'),
                           'positions2': np.argwhere(self.board1 == player + '2'),
                           'king_positions2': np.argwhere(self.board1 == player + '2k')
                           },
                'board2': {'positions1': np.argwhere(self.board2 == player + '1'),
                           'king_positions1': np.argwhere(self.board2 == player + '1k'),
                           'positions2': np.argwhere(self.board2 == player + '2'),
                           'king_positions2': np.argwhere(self.board2 == player + '2k')}}

    def get_move_state(self, row_dir_list, positions, board):
        one_move_board = []
        one_move_list=[]
        for position in positions:
            for row_dir in row_dir_list:
                next_row = position[0] + row_dir
                for dir in [-1,1]:
                    next_col = position[1] + dir
                    if board[next_row, next_col] == '.':
                        next_one_move = self.update_board(position, [next_row, next_col], board, False)
                        one_move_board.append(next_one_move)
                        one_move_list.append([next_row, next_col])
                    if board[next_row, next_col][0] == self.opponent:
                        if board[next_row + row_dir, next_col + dir] == '.':
                            next_capture_move = self.update_board(position, [next_row + row_dir, next_col + dir],
                                                                      board, True)
                            one_move_board.append(next_capture_move)
                            one_move_list.append([next_row + row_dir, next_col + dir])
        return one_move_list,one_move_board

    def get_two_move_state(self,one_move_list,one_move_board,row_dir):
        two_move_board=[]
        for i in range(len(one_move_list)):
            _,sencond_move=self.get_move_state(row_dir,[one_move_list[i]],one_move_board[i])
            two_move_board.append(sencond_move)
        return two_move_board

    def update_board(self, position, next_position, board, capture):
        board_temp = copy.deepcopy(board)
        board_temp[position[0], position[1]] = '.'
        board_temp[next_position[0], next_position[1]] = board[position[0], position[1]]  # change to king
        if capture:
            board_temp[position[0], position[1]] = '.'
            board_temp[next_position[0], next_position[1]] = board[position[0], position[1]]
            board_temp[int((position[0] + next_position[0]) / 2), int((position[1] + next_position[1]) / 2)] = '.'
        return board_temp


    def move_list(self):
        one_move_list_nomarl1,one_move_board_normal1=self.get_move_state( [self.direction],np.concatenate((self.positions['board1']['positions1'], self.positions['board1']['positions2'])),self.board1)
        one_move_list_nomarl2,one_move_board_normal2=self.get_move_state([self.direction], np.concatenate((self.positions['board2']['positions1'], self.positions['board2']['positions2'])), self.board2)
        one_move_list_king1,one_move_board_king1=self.get_move_state( [1,-1],np.concatenate((self.positions['board1']['king_positions1'], self.positions['board1']['king_positions2'])),self.board1)
        one_move_list_king2,one_move_board_king2=self.get_move_state( [1,-1],np.concatenate((self.positions['board2']['king_positions1'], self.positions['board2']['king_positions2'])),self.board2)
        two_move_board_normal1=self.get_two_move_state(one_move_list_nomarl1,one_move_board_normal1,[self.direction])
        two_move_board_normal2 = self.get_two_move_state(one_move_list_nomarl2,one_move_board_normal2,[self.direction])
        two_move_board_king1 = self.get_two_move_state(one_move_list_king1, one_move_board_king1,[1,-1])
        two_move_board_king2 = self.get_two_move_state(one_move_list_king2, one_move_board_king2,[1,-1])
        return one_move_board_normal1+one_move_board_normal2+one_move_board_king1+one_move_board_king2+two_move_board_normal1+two_move_board_normal2+two_move_board_king1+two_move_board_king2




if __name__ == '__main__':
    board1 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, 'w1', '.', 'w1', '.', 1],
                       [1, '.', 'b1', '.', '.', 1],
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
