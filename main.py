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


    game = playGame(WINDOW)
    mxplayer1 = MinimaxPlayer(WHITE, 'capture', 1)
    mxplayer2 = MinimaxPlayer(BLACK, 'capture', 1)
    rdplayer1 = randomPlayer(WHITE)
    rdplayer2 = randomPlayer(BLACK)


    # game_type:
    # 1:hvh 2:hvr 3:hva 4:rva 5:ava
    game_type = 4
    if game_type==4:
        game = playGame(WINDOW)
        player1 = randomPlayer(WHITE)
        player2 = MinimaxPlayer(BLACK, 'capture', 3)
        while run:
            clock.tick(60)

            next_move = player1.get_next_move(game.gs)
            game.computer_move(next_move)
            game_result = game.gs.check_win(next_move)

            if game.game_over():
                run = False

            next_move = player2.get_next_move(game.gs)
            game.computer_move(next_move)
            game_result = game.gs.check_win(next_move)

            if game.game_over():
                run = False

            game.update()

        pygame.quit()







    # while run:
    #     clock.tick(60)
    #
    #     if game.turn == WHITE:
    #         value, new_board = minimax(game.get_board(), 4, WHITE, game)
    #         game.ai_move(new_board)
    #
    #     if game.winner() != None:
    #         print(game.winner())
    #         run = False
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             pos = pygame.mouse.get_pos()
    #             row, col = get_row_col_from_mouse(pos)
    #             game.select(row, col)
    #
    #     game.update()
    #
    # pygame.quit()
    #
    #
    # while run:
    #     clock.tick(60)
    #     if game.gs.player == computer.color:
    #         next_move = computer.get_next_move(game.gs)
    #         game.ai_move(next_move)
    #
    #     if gs:
    #         print(game.winner())
    #         run = False
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #
    #         if player.gs.player == BLACK:
    #             next_move = rdplayer1.get_next_move(player.gs)
    #             player.ai_move(next_move)
    #
    #     if random:
    #         if  player.gs.player == WHITE:
    #             next_move = rdplayer.get_next_move(player.gs)
    #             player.ai_move(next_move)
    #
    #     if not cvc:
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             pos = pygame.mouse.get_pos()
    #             row, col = get_row_col_from_mouse(pos)
    #             game.select(row, col)
    #
    #     game.update()
    #
    # pygame.quit()


