"""
IS597DS - Final Project
Authors: Yawen Deng, Candice Chen

Title: Parallel-Universes Checkers

UI Reference:
Our UI mainly referred to this source:
https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/game.py

"""

import pygame
from checkers.cons import SQUARE_SIZE, WIDTH, HEIGHT, WHITE, BLACK
from checkers.playGame import playGame
from checkers.player import randomPlayer, MinimaxPlayer


# def one_turn(player, game):
#     next_move_options = game.get_valid_moves()
#     next_move, mode = player.get_next_move(next_move_options)
#     game_result = game.check_win(next_move)
#     if game_result == WHITE or game_result == BLACK:
#         player.win_count += 1
#         return False
#     if game_result == 'draw':
#         return False
#     print('player:', game.player, 'next_move:', next_move)
#     for move in next_move:
#         if move['start_board'] != move['end_board']:
#             new_board1, new_board2 = game.transfer_piece(move, make_move=True)
#         else:
#             if move['start_board'] == 1:
#                 new_board1 = game.update_board_normal(move, game.boards.board1, make_move=True)
#                 new_board2 = game.boards.board2
#             else:
#                 new_board2 = game.update_board_normal(move, game.boards.board2, make_move=True)
#                 new_board1 = game.boards.board1
#
#     return new_board1, new_board2


# def one_round(player1, player2):
#     boards = Boards()
#     game = GameState(player1.color, boards, 0)
#     while True:
#         result = one_turn(player1, game)
#         if result:
#             new_board1, new_board2 = result
#             game.boards.board1 = new_board1
#             game.boards.board2 = new_board2
#             game = GameState(player2.color, game.boards, game.no_capture)
#         else:
#             break
#
#         result = one_turn(player2, game)
#         if result:
#             new_board1, new_board2 = result
#             game.boards.board1 = new_board1
#             game.boards.board2 = new_board2
#             game = GameState(player1.color, game.boards, game.no_capture)
#         else:
#             break
#     print('=======')
#     for a, b in zip(game.boards.board1, game.boards.board2):
#         print('%s   %s' % ((' '.join('%03s' % i for i in a), (' '.join('%03s' % i for i in b)))))


def print_stat(stats):
    """
    Print tha final statistic.
    """
    num_rounds = len(stats)
    gap = 1
    if num_rounds > 500:
        gap = 50
    print('\n\n')
    print('{:^20s} {:^10s} {:^10s} {:^20s} {:^10s} {:^10s} {:^10s}'.format(' # Player1 ', ' # Won ', '%', ' # Player2 ',
                                                                           ' # Won ', '%', '# Draw'))
    print('{:^20s} {:^10s} {:^10s} {:^20s} {:^10s} {:^10s} {:^10s}'.format('--------------------', '----------',
                                                                           '----------', '--------------------',
                                                                           '----------',
                                                                           '----------', '----------'))

    for result in stats:
        for key, value in result.items():
            if num_rounds // gap == key:
                draw = num_rounds - value["win1"] - value["win2"]
                win_percent1 = value["win1"] / num_rounds * 100
                win_percent2 = value["win2"] / num_rounds * 100
                print('{:^20s} {:^10} {:^10} {:^20s} {:^10} {:1^0} {:^10}'.format(
                    value["tag1"], value["win1"], win_percent1, value["tag2"], value["win2"],
                    win_percent2, draw))

def print_game_result(game, player1, player2):

    board1 = game.gs.boards.board1
    board2 = game.gs.boards.board2
    winner = 'WHITE' if game.gs.opponent == WHITE else 'BLACK'
    draw=False
    if game.gs.no_capture >= 100:
        dif = game.gs.independent_universe[game.gs.player] - game.gs.independent_universe[game.gs.opponent]
        if dif == 0:
            draw = True
        else:
            win = game.gs.player if dif > 0 else game.gs.opponent
            winner = 'WHITE' if win == WHITE else 'BLACK'

    if winner == player1.color:
        player1.win_count += 1
    else:
        player2.win_count += 1

    print("\n=========  Game Over  =========")
    if draw:
        print("\nIt's a draw.")
    else:
        print("\n {} wins!".format(winner))
    print('\nFinal Boards')
    for a, b in zip(board1, board2):
        print('%s | %s' % ((' '.join('%07s' % i for i in a), (' '.join('%07s' % i for i in b)))))


def run_games(game_type, rounds):

    if game_type == 1:
        computer = randomPlayer(WHITE)
    elif game_type == 2:
        computer = MinimaxPlayer(WHITE, 'capture', 2)
    elif game_type == 3:
        player1 = randomPlayer(WHITE)
        player2 = MinimaxPlayer(BLACK, 'capture', 3)

    elif game_type == 4:
        player1 = randomPlayer(WHITE)
        player2 = MinimaxPlayer(BLACK, 'king', 3)
    else:
        player1 = MinimaxPlayer(WHITE, 'capture', 3)
        player2 = MinimaxPlayer(BLACK, 'king', 3)

    stats = []
    for i in range(rounds):
        run = True
        clock = pygame.time.Clock()
        WINDOW = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
        game = playGame(WINDOW)

        if game_type in [1, 2]:
            while run:
                clock.tick(60)

                if game.gs.player == WHITE:
                    next_move = computer.get_next_move(game)
                    game.computer_move(next_move)

                if game.gs.game_over():
                    run = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col, board_num = game.get_row_col_from_mouse(pos)
                        next_move = game.select(row, col, board_num)

                if game.gs.game_over():
                    run = False
                game.update_window()


        if game_type in [3, 4, 5]:
            while run:
                clock.tick(60)

                next_move = player1.get_next_move(game)
                game.computer_move(next_move)
                game.update_window()
                if game.gs.game_over():
                    run = False

                next_move = player2.get_next_move(game)
                game.computer_move(next_move)
                game.update_window()
                if game.gs.game_over():
                    run = False

                game.update_window()

            pygame.quit()
            result = {"tag1": player1.player_tag, "win1": player1.win_count, "tag2": player2.player_tag,
                     "win2": player2.win_count}
            stats.append(result)

        print_game_result(game, player1, player2)

    # print_stat(stats)

if __name__ == '__main__':


    # current board size = 6
    # (using ROWS in cons.py to change board size)

    # game_type:
    # 1: Human vs random player
    # 2: Human vs Minimax player
    # 3: Random player vs Aggressive player
    # 4: Random player vs Lion-King player
    # 5: Aggressive player vs Lion-King player
    game_type = 3

    run_games(game_type=game_type, rounds=5)