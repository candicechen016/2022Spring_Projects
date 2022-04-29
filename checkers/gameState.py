"""
Game state module.
"""

import copy

import pygame

from checkers.cons import WHITE, BLACK, ROWS


class GameState:
    def __init__(self, player, boards, no_capture=0):

        self.boards = boards
        self.player = player
        self.opponent = BLACK if self.player == WHITE else WHITE
        self.capture_count = 0
        self.no_capture = no_capture
        self.reset()


    def reset(self):

        self.positions = {'board1': self.get_positions(self.player, self.boards.board1),
                          'board2': self.get_positions(self.player, self.boards.board2)}
        self.opponent_positions = {'board1': self.get_positions(self.opponent, self.boards.board1),
                                   'board2': self.get_positions(self.opponent, self.boards.board2)}

    def get_positions(self, color, board):
        positions1 = []
        for i in range(1, ROWS + 1):
            for j in range(1, ROWS + 1):
                piece = board[i][j]
                if piece != 0 and piece.color == color:
                    positions1.append(piece)
        return positions1

    def one_move(self, row_dirs, position, board, board_num, captured=[], transfer=False):
        next_moves = []
        captured_left = False
        for row_dir in row_dirs:
            next_row = position[0] + row_dir
            for col_dir in [-1, 1]:
                next_col = position[1] + col_dir
                next_position = board[next_row][next_col]
                if next_position == 1:
                    continue
                elif next_position == 0:
                    if not captured:
                        next_move = {'end_move': [next_row, next_col], 'end_board': board_num, 'capture': captured}
                        next_moves.append(next_move)
                elif next_position.color == self.opponent and not transfer:
                    if board[next_row + row_dir][next_col + col_dir] == 0:
                        print('-------------------------------------------')
                        print('postion',position)
                        captured.append([next_row, next_col])
                        print('captured:',captured)
                        piece = board[next_row][next_col]
                        board[next_row][next_col] = 0
                        if col_dir == -1:
                            captured_left = True
                        if (next_row + row_dir == ROWS and self.player == WHITE) or (
                                next_row + row_dir == 1 and self.player == BLACK):
                            row_dirs = [-1, 1]
                        moves = self.one_move(row_dirs, [next_row + row_dir, next_col + col_dir], board, board_num,
                                              captured, transfer)
                        next_moves += moves
                        del captured[-1]
                        board[next_row][next_col] = piece
        if captured_left == False and captured:
            next_move = {'end_move': [position[0], position[1]], 'end_board': board_num,
                         'capture': copy.deepcopy(captured)}
            next_moves.append(next_move)
        return next_moves

    def get_moves(self, piece, board, board_num):
        one_move_list = []
        # one_move_boards = []
        two_move_list = []
        # two_move_boards = []
        row, col = piece.row, piece.col
        end_moves = self.one_move(piece.direction, [row, col], board, board_num)
        for m in end_moves:
            m['start_move'] = [row, col]
            m['start_board'] = board_num
            one_move_board = self.update_board_normal(m, board)
            one_move_list.append(m)
            # one_move_boards.append(one_move_board)
            second_moves = self.one_move(one_move_board[m['end_move'][0]][m['end_move'][1]].direction,
                                         m['end_move'],one_move_board, board_num)
            if second_moves:
                for n in second_moves:
                    n['start_move'] = m['end_move']
                    n['start_board'] = board_num
                    # second_board = self.update_board_normal(n, one_move_board)
                    two_move_list.append([m, n])
                    # two_move_boards.append(second_board)
        return one_move_list, two_move_list

    def update_king(self, piece, position):
        if position[0] == ROWS and piece.color == WHITE:
            piece.make_king()
            self.boards.w_king_left += 1
        elif position[0] == 1 and piece.color == BLACK:
            piece.make_king()
            self.boards.b_king_left += 1

    def update_board_normal(self, move, board, make_move=False):
        if make_move:
            board_temp = board
        else:
            board_temp = copy.deepcopy(board)
        start_piece = board_temp[move['start_move'][0]][move['start_move'][1]]
        board_temp[move['end_move'][0]][move['end_move'][1]] = start_piece
        if make_move:
            start_piece.move(move['end_move'][0], move['end_move'][1])
            self.capture_count += len(move['capture'])
        board_temp[move['start_move'][0]][move['start_move'][1]] = 0

        self.update_king(start_piece, move['end_move'])

        if move['capture']:

            for cap in move['capture']:
                if board_temp[cap[0]][cap[1]].color == WHITE:
                    self.boards.w_left_ = -1
                    if cap[0] == ROWS - 1:
                        start_piece.make_king()
                        self.boards.w_king_left += 1
                else:
                    self.boards.b_left -= 1
                    if cap[0] == 2:
                        start_piece.make_king()
                        self.boards.b_king_left += 1
                board_temp[cap[0]][cap[1]] = 0
        return board_temp

    def find_orthogonally_neighbors(self, piece_position, board):
        x, y = piece_position
        neighbors = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        empty = []
        for n in neighbors:
            if board[n[0]][n[1]] == 0:
                empty.append(n)
        return empty

    def transfer_piece(self, move_dict, make_move=False):
        # start_board = self.boards.board1 if move_dict['start_board'] == 1 else self.boards.board2
        if move_dict['start_board']==1:
            start_board = self.boards.board1
            end_board = self.boards.board2
        else:
            start_board = self.boards.board2
            end_board = self.boards.board1
        # end_board = self.boards.board1 if move_dict['end_board'] == 1 else self.boards.board2

        if not make_move:
            start_board = copy.deepcopy(start_board)
            end_board = copy.deepcopy(end_board)

        start_move, end_move = move_dict['start_move'], move_dict['end_move']
        piece = start_board[start_move[0]][start_move[1]]
        start_board[start_move[0]][start_move[1]] = 0
        end_board[end_move[0]][end_move[1]] = piece
        if make_move:
            piece.move(end_move[0], end_move[1])
            piece.board_num=move_dict['end_board']
            piece.calc_pos()
        self.update_king(piece, [end_move[0], end_move[1]])
        return start_board, end_board

    def get_transferred_list(self, piece, board_num):
        end_board_num = 2 if board_num == 1 else 1
        other_board = self.boards.board2 if board_num == 1 else self.boards.board1
        transfer_move_list = []
        # transfer_board_list = []

        list = self.find_orthogonally_neighbors([piece.row, piece.col], other_board)
        for move in list:
            to_move = {'start_move': [piece.row, piece.col], 'start_board': board_num, 'end_move': move,
                           'end_board': end_board_num, 'capture':[]}

            new_start_board, new_end_board = self.transfer_piece(to_move)

            second_move_list = self.one_move(new_end_board[move[0]][move[1]].direction, move, new_end_board,
                                                 end_board_num, transfer=True)
            if second_move_list:
                for m in second_move_list:
                    m['start_move'] = move
                    m['start_board'] = end_board_num
                        # second_move_board=self.update_board_normal(m,new_end_board)
                        # transfer_board_list.append(second_move_board)
                    transfer_move_list.append([to_move, m])
        return transfer_move_list

    def get_valid_moves_piece(self,piece,board,board_num):
        one_move_list, two_move_list, = self.get_moves(piece, board, board_num)
        transfer_move_list= self.get_transferred_list(piece, board_num)
        return one_move_list,two_move_list,transfer_move_list

    def get_valid_moves(self):
        one_move_list1=[]
        one_move_list2=[]
        two_move_list=[]
        transfer_move_list=[]
        self.reset()
        for b in ['board1','board2']:
            for piece in self.positions[b]:
                board=self.boards.board1 if b=='board1' else self.boards.board2
                board_num=1 if b=='board1' else 2
                one_moves,two_moves,transfer_moves=self.get_valid_moves_piece(piece,board,board_num)
                # if player:
                #     player.gs.boards.draw_board(player.win)
                #     print('piece:',[piece.row,piece.col])
                #     pygame.draw.circle(player.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
                #     one_move_list = [[m] for m in one_moves]
                #     valid_moves = one_move_list + two_moves + transfer_moves
                #     player.draw_valid_moves(valid_moves)
                #     pygame.display.update()
                #     pygame.time.delay(500)

                if b=='board1':
                    one_move_list1+=one_moves
                else:
                    one_move_list2+=one_moves
                two_move_list+=two_moves
                transfer_move_list+=transfer_moves
        one_move_comb = self.first_move_comb(one_move_list1, one_move_list2)
        return {'one_move': one_move_comb,'two_move': two_move_list, 'transfer_move': transfer_move_list}

    def get_all_valid_moves(self):
        all_moves = []
        for key, value in self.get_valid_moves().items():
            all_moves += value
        return all_moves

    def check_win(self, next_move):
        has_pieces = 0

        # condition 1: the player has NO STEPS and NO WAY to transfer to both boards
        if not next_move:
            print('no_moves:', self.opponent)
            return self.opponent

        for board_name in ['board1', 'board2']:
            # condition 2: the player has NO PIECES on Both boards
            if len(self.positions[board_name]) == 0:
                has_pieces += 1
                continue
        if has_pieces == 2:
            print('No piece:', self.opponent)
            return self.opponent
        # draw: no capture in 50 turns
        for move in next_move:
            if not move['capture']:
                self.no_capture += 1
            else:
                self.no_capture = 0
        if self.no_capture >= 50:
            print('draw')
            return 'draw'
        return False

    def first_move_comb(self, moves1, moves2):
        one_move_list = []
        for m in moves1:
            for n in moves2:
                one_move_list.append([m, n])
        return one_move_list

    # refer

    def evaluation(self, strategy='kings'):
        score=0
        if strategy == 'kings':
            score = self.strategy_more_kings(self.player)
            print("strategy_more_kings",score)

        if strategy == 'capture':
            score = self.strategy_capture()
        return score

    def strategy_more_kings(self, player):
        if player == WHITE:
            my_piece_total, opponent_piece_total = self.boards.w_left, self.boards.b_left
            my_king, opponent_king = self.boards.w_king_left, self.boards.b_king_left
        if player == BLACK:
            my_piece_total, opponent_piece_total = self.boards.b_left, self.boards.w_left
            my_king, opponent_king = self.boards.b_king_left, self.boards.w_king_left
        score = my_piece_total - opponent_piece_total + my_king * 1.5 - opponent_king * 1.5
        return score

    def strategy_capture(self):
        return self.capture_count

