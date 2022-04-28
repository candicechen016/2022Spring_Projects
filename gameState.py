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
import random

import copy

import pygame.draw

from main3 import WHITE, BLACK, ROWS, COLS, GOLD, SILVER, Boards, Piece, BLUE, GREEN, YELLOW, SQUARE_SIZE, WIDTH, HEIGHT


class GameState:

    def __init__(self, win,player, boards, no_capture=0):

        self.win=win
        self.boards=boards
        self.board1 = boards.board1
        self.board2 = boards.board2
        self.player = player
        self.opponent = BLACK if self.player == WHITE else WHITE
        # self.w_left = self.b_left=12
        self.no_capture = no_capture
        self.positions = {'board1': self.get_positions(self.player, self.board1),
                          'board2': self.get_positions(self.player, self.board2)}
        self.opponent_positions = {'board1': self.get_positions(self.opponent, self.board1),
                                   'board2': self.get_positions(self.opponent, self.board2)}

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
                        captured.append([next_row, next_col])
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



    def get_moves(self, positions, board, board_num):
        one_move_list = []
        # one_move_boards = []
        two_move_list = []
        # two_move_boards = []
        for piece in positions:
            row,col=piece.row,piece.col
            end_moves = self.one_move(piece.direction, [row,col], board, board_num)
            for m in end_moves:
                m['start_move'] = [row,col]
                m['start_board'] = board_num
                one_move_board = self.update_board_normal(m, board)
                one_move_list.append(m)
                # one_move_boards.append(one_move_board)
                second_moves = self.one_move(one_move_board[m['end_move'][0]][m['end_move'][1]].direction,
                                             m['end_move'],
                                             one_move_board, board_num)
                if second_moves:
                    for n in second_moves:
                        n['start_move'] = m['end_move']
                        n['start_board'] = board_num
                        # second_board = self.update_board_normal(n, one_move_board)
                        two_move_list.append([m, n])
                        # two_move_boards.append(second_board)
        return one_move_list,two_move_list

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
        board_temp[move['start_move'][0]][move['start_move'][1]] = 0

        self.update_king(start_piece, move['end_move'])

        if move['capture']:
            for cap in move['capture']:
                if board_temp[cap[0]][cap[1]].color == WHITE:
                    self.boards.w_left_ = 1
                    if cap[1] == ROWS - 1:
                        start_piece.make_king()
                        self.boards.w_king_left += 1
                else:
                    self.boards.b_left -= 1
                    if cap[1] == 2:
                        start_piece.make_king()
                        self.boards.b_king_left += 1
                board_temp[cap[0]][cap[1]] = 0
        return board_temp

    def find_orthogonally_neighbors(self, piece_position, board):
        x, y = piece_position
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        empty = []
        for n in neighbors:
            if board[n[0]][n[1]]== 0:
                empty.append(n)
        return empty

    def transfer_piece(self, move_dict, make_move=False):
        board1 = self.board1 if move_dict['start_board'] == 1 else self.board2
        board2 = self.board1 if move_dict['end_board'] == 1 else self.board2

        if make_move:
            start_board = board1
            end_board = board2
        else:
            start_board = copy.deepcopy(board1)
            end_board = copy.deepcopy(board2)

        start_move, end_move = move_dict['start_move'], move_dict['end_move']
        piece = board1[start_move[0]][start_move[1]]
        start_board[start_move[0]][start_move[1]] = 0
        end_board[end_move[0]][end_move[1]] = piece
        if make_move:
            piece.move(end_move[0], end_move[1])
        self.update_king(piece, [end_move[0], end_move[1]])
        return start_board, end_board

    def get_transferred_list(self, positions, board_num):
        end_board_num = 2 if board_num == 1 else 1
        other_board = self.board2 if board_num == 1 else self.board1
        transfer_move_list = []
        # transfer_board_list = []

        for piece in positions:
            list = self.find_orthogonally_neighbors([piece.row, piece.col], other_board)
            for move in list:
                to_move = {'start_move': [piece.row, piece.col], 'start_board': board_num, 'end_move': move,
                           'end_board': end_board_num, 'capture': ''}

                new_start_board, new_end_board = self.transfer_piece(to_move)

                second_move_list = self.one_move(new_end_board[move[0]][move[1]].direction, move, new_end_board,
                                                                        end_board_num,transfer=True)
                if second_move_list:
                    for m in second_move_list:
                        m['start_move']=move
                        m['start_board']=end_board_num
                        # second_move_board=self.update_board_normal(m,new_end_board)
                        # transfer_board_list.append(second_move_board)
                        transfer_move_list.append([to_move, m])
        return transfer_move_list

    def get_valid_moves(self):
        one_move_list1, two_move_list1, = self.get_moves(
            self.positions['board1'], self.board1, 1)
        one_move_list2, two_move_list2,= self.get_moves(
            self.positions['board2'], self.board2, 2)
        one_move_comb=self.first_move_comb(one_move_list1,one_move_list2)
        transfer_move_list1=self.get_transferred_list(self.positions['board1'],1)
        transfer_move_list2 = self.get_transferred_list(self.positions['board2'], 2)
        return {'one_move': one_move_comb,
                'two_move': two_move_list1 + two_move_list2, 'transfer_move':transfer_move_list1+transfer_move_list2}

    def check_win(self, next_move):
        has_pieces = 0

        # condition 1: the player has NO STEPS and NO WAY to transfer to both boards
        if not next_move:
            print('no_moves:', self.opponent)
            return self.opponent

        for board_name in ['board1', 'board2']:
            # condition 2: the player has NO PIECES on Both boards
            if len(self.positions) == 0:
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

    def first_move_comb(self,moves1,moves2):
        one_move_list=[]
        for m in moves1:
            for n in moves2:
                one_move_list.append([m,n])
        return one_move_list


    #refer
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


def one_turn(player, game):
    next_move_options = game.get_valid_moves()
    next_move,mode = player.get_next_move(next_move_options)
    game_result = game.check_win(next_move)
    if game_result == WHITE or game_result == BLACK:
        player.win_count += 1
        return False
    if game_result == 'draw':
        return False
    print('player:', game.player, 'next_move:', next_move)
    for move in next_move:
        if move['start_board'] != move['end_board']:
            new_board1, new_board2 = game.transfer_piece(move, make_move=True)
        else:
            if move['start_board'] == 1:
                new_board1 = game.update_board_normal(move, game.board1,make_move=True)
                new_board2 = game.board2
            else:
                new_board2 = game.update_board_normal(move, game.board2, make_move=True)
                new_board1 = game.board1
    print('=======')

    print(new_board1)
    print(new_board2)
    print('game', game.no_capture)
    return new_board1, new_board2


def one_round(win,player1, player2):
    boards = Boards()
    game = GameState(win,player1.color, boards, 0)
    while True:
        result = one_turn(player1, game)
        if result:
            new_board1, new_board2 = result
            game.boards.board1=new_board1
            game.boards.board2=new_board2
            game = GameState(game.win,player2.color,game.boards, game.no_capture)
        else:
            break

        result = one_turn(player2, game)
        if result:
            new_board1, new_board2 = result
            game.boards.board1 = new_board1
            game.boards.board2 = new_board2
            game = GameState(game.win,player1.color, game.boards, game.no_capture)
        else:
            break


class MinimaxPlayer:

    def __init__(self, piece, ai=False, strategy=0):
        self.piece = piece
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0

    def minimax_moves(self, next_move_options):
        pass

#
def main():
    WIN = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
    player1 = randomPlayer(WHITE)
    player2 = randomPlayer(BLACK)
    for i in range(5):
        print(i)
        one_round(WIN,player1, player2)
    print(player1.win_count)
    print(player2.win_count)
    # gs.board1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #              [1, 0, 0, 0, 0, Piece(1, 5, WHITE, 1), 0, 0, 0, 1],
    #              [1, 0, 0, 0, Piece(2, 4, BLACK, 1), 0, Piece(2, 6, BLACK, 1), 0, 0, 1],
    #              [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #              [1, 0, Piece(4, 2, BLACK, 1), 0, 0, 0, 0, 0, 0, 1],
    #              [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #              [1, 0, 0, 0, 0, Piece(6, 5, WHITE, 1), 0, 0, 0, 1],
    #              [1, 0, Piece(7, 2, BLACK, 1), 0, Piece(7, 4, BLACK, 1), 0, 0, 0, 0, 1],
    #              [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    # next_moves = gs.one_move([1], [1, 5], gs.board1, 1)

    # moves = gs.get_valid_moves()
    # for m in moves['transfer_move']:
    #     print(m)

    # for m in moves['two_move']:
    #     print(m)


#     clock = pygame.time.Clock()
# #
#     while run:
#         clock.tick(FPS)
#         for event in pygame.event.get():
#              if event.type==pygame.QUIT:
#                  run=False
#         boards.draw_board(WIN)
#         pygame.display.update()
#     pygame.quit()
main()
#
# if __name__ == '__main__':
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



#
#

#     board1 = np.array([[1, 1, 1, 1, 1, 1],
#                        [1, 'w1', '.', 'w1', '.', 1],
#                        [1, '.', '.', '.', '.', 1],
#                        [1, '.', '.', '.', '.', 1],
#                        [1, '.', 'b1', '.', 'b1', 1],
#                        [1, 1, 1, 1, 1, 1]])
#
#     board2 = np.array([[1, 1, 1, 1, 1, 1],
#                        [1, '.', 'w2', '.', 'w2', 1],
#                        [1, '.', '.', '.', '.', 1],
#                        [1, '.', '.', '.', '.', 1],
#                        [1, 'b2', '.', 'b2', '.', 1],
#                        [1, 1, 1, 1, 1, 1]])



