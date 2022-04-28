"""
UI reference: https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
"""

import pygame

from checkers.cons import SQUARE_SIZE, WIDTH, HEIGHT, WHITE, BLACK
from checkers.elements import Boards

#refer
from checkers.gameState import GameState
from checkers.player import randomPlayer


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

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

def test():
    WIN = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
    player1 = randomPlayer(WHITE)
    player2 = randomPlayer(BLACK)
    for i in range(5):
        print(i)
        one_round(WIN,player1, player2)
    print(player1.win_count)
    print(player2.win_count)

test()
    # boards=Boards()
    # gs=GameState(WIN,WHITE,boards)
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
    # for m in gs.board1:
    #     print(m)
    # next_moves = gs.one_move([1], [6, 5], gs.board1, 1)
    # for i in next_moves:
#     #     print(i)
# def main():
#     run=True
#     boards=Boards()
#     clock = pygame.time.Clock()
#     WIN= pygame.display.set_mode((WIDTH*2+2*SQUARE_SIZE, HEIGHT))
#
#     while run:
#         clock.tick(60)
#         for event in pygame.event.get():
#              if event.type==pygame.QUIT:
#                  run=False
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             pos = pygame.mouse.get_pos()
#             # row, col = get_row_col_from_mouse(pos)
#             # game.select(row, col)
#             boards.draw_board(WIN)
#
#         pygame.display.update()
#
#
#
#     pygame.quit()
# main()