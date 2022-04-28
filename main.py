"""
UI reference: https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
"""

import pygame

from checkers.cons import SQUARE_SIZE, WIDTH, HEIGHT, WHITE, BLACK, ROWS
from checkers.elements import Boards

#refer
from checkers.gameState import GameState
from checkers.player import randomPlayer, humanPlayer


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE+1
    col = x // SQUARE_SIZE
    board_num=1
    if col>ROWS+1:
        col=col-ROWS-1
        board_num=2
    return row, col,board_num

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


def one_round(player1, player2):
    boards = Boards()
    game = GameState(player1.color, boards, 0)
    while True:
        result = one_turn(player1, game)
        if result:
            new_board1, new_board2 = result
            game.boards.board1=new_board1
            game.boards.board2=new_board2
            game = GameState(player2.color,game.boards, game.no_capture)
        else:
            break

        result = one_turn(player2, game)
        if result:
            new_board1, new_board2 = result
            game.boards.board1 = new_board1
            game.boards.board2 = new_board2
            game = GameState(player1.color, game.boards, game.no_capture)
        else:
            break

# def test():
#     WIN = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
#     player1 = randomPlayer(WHITE)
#     player2 = randomPlayer(BLACK)
#     for i in range(5):
#         print(i)
#         one_round(player1, player2)
#     print(player1.win_count)
#     print(player2.win_count)
#
# test()

def main():
    run=True
    boards=Boards()
    clock = pygame.time.Clock()
    WIN= pygame.display.set_mode((WIDTH*2+2*SQUARE_SIZE, HEIGHT))
    mode='huamn'
    gs = GameState(WHITE, boards, 0)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
             if event.type==pygame.QUIT:
                 run=False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col,board_num = get_row_col_from_mouse(pos)
            if mode=='huamn':
                player=humanPlayer(WIN,gs)
                player.select(row, col,board_num)
                boards.draw_board(WIN)

        pygame.display.update()

    pygame.quit()
main()