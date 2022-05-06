"""

IS597DS - Final Project
Authors: Yawen Deng, Candice Chen

==Parallel-Universes Checkers==

UI Reference:
Our UI mainly referred to this source:
https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
We tried to make the UI fit our game so the some elements in our structure

#king direction prob
"""

import pygame

from checkers.cons import SQUARE_SIZE, WIDTH, HEIGHT, WHITE, BLACK, ROWS
from checkers.elements import Boards

from checkers.gameState import GameState
from checkers.playGame import playGame
from checkers.player import randomPlayer, humanPlayer, MinimaxPlayer

def one_turn(player, game):
    next_move_options = game.get_valid_moves()
    next_move, mode = player.get_next_move(next_move_options)
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
                new_board1 = game.update_board_normal(move, game.boards.board1, make_move=True)
                new_board2 = game.boards.board2
            else:
                new_board2 = game.update_board_normal(move, game.boards.board2, make_move=True)
                new_board1 = game.boards.board1

    # print('=======')
    # for a, b in zip(new_board1, new_board2):
    #     print('%s   %s' % ((' '.join('%03s' % i for i in a), (' '.join('%03s' % i for i in b)))))
    # print(new_board1)
    # print(new_board2)
    print('game', game.no_capture)
    return new_board1, new_board2

def print_stat(stats):
    """
    Print tha final learning statistic.
    """
    num_rounds = len(stats)
    gap = 10
    if num_rounds > 500:
        gap = 50
    print()
    print('{:^20s} {:^10s} {:^10s} {:^20s} {:^10s} {:^10s} {:^10s}'.format(' # Player1 ', ' # Won ', '%', ' # Player2 ',
                                                                           ' # Won ', '%', '# Draw'))
    print('{:^20s} {:^10s} {:^10s} {:^20s} {:^10s} {:^10s} {:^10s}'.format('--------------------', '----------',
                                                                           '----------', '--------------------',
                                                                           '----------',
                                                                           '----------', '----------'))
    for key, value in stats.items():
        if num_rounds // gap == key:
            draw = num_rounds - value["win1"] - value["win2"]
            win_percent1 = value["win1"] / num_rounds * 100
            win_percent2 = value["win2"] / num_rounds * 100
            print('{:^20s} {:^10} {:^10} {:^20s} {:^10} {:1^0} {:^10}'.format(
                value["tag1"], value["win1"], win_percent1, value["tag2"], value["win2"],
                win_percent2, draw))

def one_round(player1, player2):
    boards = Boards()
    game = GameState(player1.color, boards, 0)
    while True:
        result = one_turn(player1, game)
        if result:
            new_board1, new_board2 = result
            game.boards.board1 = new_board1
            game.boards.board2 = new_board2
            game = GameState(player2.color, game.boards, game.no_capture)
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
    print('=======')
    for a, b in zip(game.boards.board1, game.boards.board2):
        print('%s   %s' % ((' '.join('%03s' % i for i in a), (' '.join('%03s' % i for i in b)))))


def playerGame(WINDOW, gs):
    pass


if __name__ == '__main__':
    run = True
    clock = pygame.time.Clock()
    WINDOW = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
    game_type=1 # 1:hvr 2:hva
    if game_type==1:
        computer=randomPlayer(WHITE)
    elif game_type==2:
        computer= MinimaxPlayer(WHITE,'capture', 3)
    game=playGame(WINDOW)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col, board_num= game.get_row_col_from_mouse(pos)
                next_move = game.select(row, col, board_num)

        if game.gs.player == WHITE:
            next_move = computer.get_next_move(game.gs)
            game.computer_move(next_move)

        game.update_window()

    pygame.quit()


