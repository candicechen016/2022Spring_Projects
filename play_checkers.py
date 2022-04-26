import numpy as np
import random
from main import GameState, randomPlayer


def initial_board(size):
    rows_with_pieces = (size - 2) / 2
    board = []
    for i in list(range(size + 2)):
        if i == 0 or i == size + 1:
            board.append(['  '] + ['---'] * (size) + ['  '])
        elif i in [rows_with_pieces + 1, rows_with_pieces + 2]:
            board.append(['|'] + ['.'] * size + ['|'])
        else:
            p = 'w1'
            if i % 2 != 0:
                if i >= (size - rows_with_pieces):
                    p = ' b1'
                board.append(['|'] + ['.', p] * (size // 2) + ['|'])
            else:
                if i >= (size - rows_with_pieces):
                    p = 'b1'
                board.append(['|'] + [p, '.'] * (size // 2) + ['|'])

    b1 = np.array(board)
    b = np.flip(b1, 1)
    c = np.where(b == 'w1', 'w2', b)
    b2 = np.where(c == 'b1', 'b2', c)
    return b1, b2


def make_move(player, game):
    next_move_options = game.move_list()
    next_move = player.get_next_move(next_move_options)
    game_result = game.check_win(next_move)
    if game_result == 'w' or game_result == 'b':
        player.win_count += 1
        print_game_result(game.board1, game.board2, player, draw=False)
        return False
    if game_result == 'draw':
        print_game_result(game.board1, game.board2, player, draw=True)
        return False
    print('player:', game.player, 'next_move:', next_move)
    for move in next_move:
        if move['start_board'] != move['end_board']:
            new_board1, new_board2 = game.transfer_piece(move, make_move=True)
        else:
            if move['start_board'] == 1:
                new_board1 = game.update_board_normal(move, make_move=True)
                new_board2 = game.board2
            else:
                new_board2 = game.update_board_normal(move, make_move=True)
                new_board1 = game.board1
    print('=======')
    for a, b in zip(new_board1, new_board2):
        print('%s   %s' % ((' '.join('%03s' % i for i in a), (' '.join('%03s' % i for i in b)))))
    print('game', game.no_capture)
    return new_board1, new_board2


def print_game_result(board1, board2, player, draw=False):
    print("\n=========  Game Over  =========")
    if draw:
        print("\nIt's draw.")
    else:
        print("\n {} wins!".format(player.name))
    for a, b in zip(board1, board2):
        print('%s   %s' % ((' '.join('%03s' % i for i in a), (' '.join('%03s' % i for i in b)))))


def play_one_round(gamestate, player1, player2, size=4):
    game = gamestate
    # game = GameState(size, player1.piece, init_board1, init_board2, no_capture=0)
    while True:
        result = make_move(player1, game)
        if result:
            new_board1, new_board2 = result
            game = GameState(size, player1.piece, new_board1, new_board2, game.no_capture)
        else:
            break
        print('GameState.count',GameState.count)
        print('player2')
        result = make_move(player2, game)
        print('result',result)
        if result:
            print('make move')
            new_board1, new_board2 = result
            game = GameState(size, player2.piece, new_board1, new_board2, game.no_capture)
        else:
            break


def print_stat(num_rounds, player1, player2):
    """
    Print tha final learning statistic.
    """
    draw = num_rounds - player1.win_count - player2.win_count
    print()
    print('{:8s} {:8s} {:8s} {:^8s}'.format(' # Player ', '# Draw', ' # Won ', '%'))
    print('{:8s} {:8s} {:8s} {:^8s}'.format('----------', '--------', '-------', '---------'))
    print('{:^8} {:^8} {:^8} {:^8.2f}%'.format(player1.name, draw, player1.win_count,
                                               player1.win_count / num_rounds * 100))
    print('{:^8} {:^8} {:^8} {:^8.2f}%'.format(player2.name, draw, player2.win_count,
                                               player2.win_count / num_rounds * 100))


if __name__ == '__main__':
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

    board1 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, 'w1', '.', 'w1', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', 'b1', '.', 'b1', 1],
                       [1, 1, 1, 1, 1, 1]])

    board2 = np.array([[1, 1, 1, 1, 1, 1],
                       [1, '.', 'w2', '.', 'w2', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, '.', '.', '.', '.', 1],
                       [1, 'b2', '.', 'b2', '.', 1],
                       [1, 1, 1, 1, 1, 1]])

    player1 = randomPlayer(piece='w')
    player2 = randomPlayer(piece='b')
    seed = 8
    random.seed(seed)

    size = 6
    init_board1, init_board2 = initial_board(size)
    game_rounds = 5
    for i in range(game_rounds):
        print(i)
        init_game = GameState(size, player1.piece, init_board1, init_board2, no_capture=0)
        play_one_round(init_game, player1, player2, size=4)

    # print(player1.win_count)
    # print(player2.win_count)
    print_stat(game_rounds, player1, player2)
