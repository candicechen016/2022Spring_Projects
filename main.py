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
import copy


class GameState:
    def __init__(self, board_size, player, board1=None, board2=None):

        if board1 is None or board2 is None:
            self.board1, self.board2 = self.initial_board(board_size)

        self.board1 = board1
        self.board2 = board2
        self.board_size = board_size
        self.player = player
        self.direction = 1 if self.player == 'w' else -1
        self.opponent = 'b' if self.player == 'w' else 'w'

        self.positions = self.get_positions(self.player)
        self.opponent_position = self.get_positions(self.opponent)

    def initial_board(self, size):
        rows_with_pieces = (size - 2) / 2
        board = []
        for i in list(range(size + 2)):
            if i == 0 or i == size + 1:
                board.append(['1'] * (size + 2))
            elif i in [rows_with_pieces + 1, rows_with_pieces + 2]:
                board.append(['1'] + ['.'] * size + ['1'])
            else:
                p = 'w1'
                if i % 2 != 0:
                    if i >= (size - rows_with_pieces):
                        p = 'b1'
                    board.append(['1'] + ['.', p] * (size // 2) + ['1'])
                else:
                    if i >= (size - rows_with_pieces):
                        p = 'b1'
                    board.append(['1'] + [p, '.'] * (size // 2) + ['1'])

        b1 = np.array(board)
        b = np.flip(b1, 1)
        c = np.where(b == 'w1', 'w2', b)
        b2 = np.where(c == 'b1', 'b2', c)
        return b1,b2




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

    def get_one_move(self, row_dir_list, positions, board, board_num):
        one_move_board = []
        one_move_list = []
        for position in positions:
            for row_dir in row_dir_list:
                next_row = position[0] + row_dir
                for dir in [-1, 1]:
                    next_col = position[1] + dir
                    if board[next_row, next_col] == '.':
                        next_one_move = self.update_board(position, [next_row, next_col], board, False)
                        one_move_board.append(next_one_move)
                        one_move_list.append({'start_move': (position[0], position[1]), 'start_board': board_num,
                                                  'end_move': (next_row, next_col),'end_board': board_num,'capture':False})
                    if board[next_row, next_col][0] == self.opponent:
                        if board[next_row + row_dir, next_col + dir] == '.':
                            next_capture_move = self.update_board(position, [next_row + row_dir, next_col + dir],
                            #                                       board, True)
                            one_move_board.append(next_capture_move)
                            one_move_list.append({'start_move': (position[0], position[1]), 'start_board': board_num,
                                                  'end_move': (next_row + row_dir, next_col + dir),'end_board': board_num,'capture':True})
        return one_move_list,one_move_board

    def get_two_continuous_move(self, one_move_list, one_move_board, row_dir):
        two_move_board = []
        two_moves=[]
        for i in range(len(one_move_list)):
            second_moves, second_move_boards = self.get_one_move(row_dir, [one_move_list[i]['end_move']], one_move_board[i],one_move_list[i]['end_board'])
            if len(second_moves):
                two_move_board.append(second_move_boards)
                for second_move in second_moves:
                    two_moves.append([one_move_list[i],second_move])
        return two_moves,two_move_board

    def update_board_normal(self, position, next_position, board, capture):
        board_temp = copy.deepcopy(board)
        player=board[position[0], position[1]]
        board_temp[position[0], position[1]] = '.'
        if (player=='w1' and position[0]==self.board_size) or (player=='b1' and position[0]==1):
            board_temp[next_position[0], next_position[1]] = player+'k'  # change to king
        else:
            board_temp[next_position[0], next_position[1]] = player
        if capture:
            board_temp[position[0], position[1]] = '.'
            board_temp[next_position[0], next_position[1]] = board[position[0], position[1]]
            board_temp[int((position[0] + next_position[0]) / 2), int((position[1] + next_position[1]) / 2)] = '.'
        return board_temp

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
                    # condition 2: the player has NO STEPS and NO WAY to transfer to both boards
                    for position in piece_positions:
                        valid_transfer_squares = self.find_orthogonally_neighbors(piece, position, board)
                        all_valid += valid_transfer_squares
        if not all_valid:
            return True

        else:
            return False

    def transfer_one_piece(self, player, position, next_position, board1, board2):
        new_board1 = copy.deepcopy(board1)
        new_board2 = copy.deepcopy(board2)
        new_board1[position[0], position[1]] = '.'
        new_board2[next_position[0], next_position[1]] = player
        return (new_board1, new_board2)

    def get_transferred_list(self, player):
        board = {1:'board1', 2:'board2'}
        end_board_num = 2
        board1 = self.board1
        board2 = self.board2
        transfer_move_list = []
        transfer_board_list = []

        for key, value in board.items():
            if key != 1:
                end_board_num = 1
            if value != 'board1':
                board1 = self.board2
                board2 = self.board1

            positions_current_board_man = self.positions[value]['positions1']
            positions_current_board_king  = self.positions[value]['king_positions1']
            for piece in positions_current_board:
                list = self.find_orthogonally_neighbors(piece, board2)
                for move in list:
                    to_move = {'start_move': (piece[0], piece[1]), 'start_board': key, 'end_move': move,
                               'end_board': end_board_num, 'capture': False}

                    next_move_board = self.transfer_piece(player, piece, move, board1, board2)

                    # TODO: determine whether 'positions1' become a king

                    [1,-1]
                    second_move_list, second_move_board = self.get_one_move(self, row_dir_list, positions, next_move_board, end_board_num)

                    if len(second_move_list):
                        transfer_board_list.append(second_move_board)
                        for second_move in second_move_list:
                            transfer_move_list.append([to_move, second_move])
                    transfer_board_list.append(second_move_board)



        return transfer_move_list

    def move_list(self):
        one_move_list_nomarl1, one_move_board_normal1 = self.get_one_move([self.direction], np.concatenate(
            (self.positions['board1']['positions1'], self.positions['board1']['positions2'])), self.board1,1)
        one_move_list_nomarl2, one_move_board_normal2 = self.get_one_move([self.direction], np.concatenate(
            (self.positions['board2']['positions1'], self.positions['board2']['positions2'])), self.board2,2)
        one_move_list_king1, one_move_board_king1 = self.get_one_move([1, -1], np.concatenate(
            (self.positions['board1']['king_positions1'], self.positions['board1']['king_positions2'])), self.board1,2)
        one_move_list_king2, one_move_board_king2 = self.get_one_move([1, -1], np.concatenate(
            (self.positions['board2']['king_positions1'], self.positions['board2']['king_positions2'])), self.board2,2)
        two_move_list_nomarl1,two_move_board_normal1 = self.get_two_continuous_move(one_move_list_nomarl1, one_move_board_normal1,
                                                         [self.direction])
        two_move_list_nomarl2,two_move_board_normal2 = self.get_two_continuous_move(one_move_list_nomarl2, one_move_board_normal2,
                                                         [self.direction])
        two_move_list_king1,two_move_board_king1 = self.get_two_continuous_move(one_move_list_king1, one_move_board_king1, [1, -1])
        two_move_list_king2,two_move_board_king2 = self.get_two_continuous_move(one_move_list_king2, one_move_board_king2, [1, -1])
        return  {'one_move_each_board':{'board1':one_move_list_nomarl1+one_move_list_king1,'board2':one_move_list_nomarl2+one_move_list_king2},
                 'two_moves_one_board':two_move_list_nomarl1+two_move_list_nomarl2+two_move_list_king1+two_move_board_king1+two_move_list_king2+two_move_board_king2}


if __name__ == '__main__':
    board1 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, 'w1', '.', 'w1', '.', 1],
                       [1, '.', 'b1', '.', '.', 1],
                       [1, '.', '.', '.', 'w1', 1],
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
    GameState(4, 'w')

    print(gs1.move_list())



    game = GameState()

    print(game.boards['1'])
    print(game.boards['2'])

    player = ['w', 'b']

    player[0].make_move()
    if game.check_win(player[0])

    # len(to_move) = 2
    # to_move =[{start_move: move,  # (x1,y1)
    #         start_board: board,  # '1'
    #         end_move: move,  # (x2,y2)
    #         end_move: board  # '2'
    #         },
    #         {
    #             start_move: move,
    #             start_board: board,
    #             end_move: move,
    #             end_move: board
    #         }]


