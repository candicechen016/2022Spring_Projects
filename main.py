"""
IS597DS - Final Project
Authors: Yawen Deng, Candice Chen

==Parallel-Universes Checkers==

Purpose:
1. Checkers with rules
2. An interactive interface to play with friends
3. Three different Machine players
    a. Random Player - randomly choose next step without any preference and strategy
    b. Lion-King Player - eager to become a king as soon as possible (I Just Can't Wait to Be King)
    c. Capture Player - tend to capture as many as possible


Variant Rules:
1. Two parallel-universes on one board for two players. We want to make the most of use of the board since the original
    version of Checkers only play at the dark squares. So a new universe is created for players to play at the dark and
    light squares at the same time. We make it more fun based on the original rules.
2. Players are allowed to do following actions during their turn:
    a. move ONE piece at the same universe TWICE (i.e. continuous two moves); continuous captures are allowed
    b. move ONE piece on EACH universe ONCE
    c. transfer ONE piece at one universe to ANOTHER universe ONCE per turn as their first or second move
    d. only allowed to transfer to an empty square and must go to an orthogonally-adjacent square on the other universe
    e. CANNOT CAPTURE at the transferring round
3. Winning conditions:
    a. Once a player has NO PIECES on both boards on his turn, he loses.
    b. Once a player has NO STEPS AND NO TRANFER options on both boards, he loses.
4. Draw condition:
    If two players keep chasing to each other without any capture for continuous 50 turns in total,
    we end the game as a draw.


UI Reference:
Our UI mainly referred to this source:
https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
We tried to make the UI fit our game so the some elements in our structure

"""

import pygame

from checkers.cons import SQUARE_SIZE, WIDTH, HEIGHT, WHITE, BLACK, ROWS
from checkers.elements import Boards, Piece

#refer
from checkers.gameState import GameState
from checkers.player import randomPlayer, humanPlayer, MinimaxPlayer


def get_row_col_from_mouse(pos):
    x, y = pos
    print(x,y)
    row = y // SQUARE_SIZE+1
    col = x // SQUARE_SIZE+1
    board_num=1
    if col>ROWS+1:
        col=col-ROWS-2
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
                                                                    '----------', '--------------------', '----------',
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

def test():
    WIN = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
    player1 = randomPlayer(WHITE)
    player2 = randomPlayer(BLACK)
    for i in range(5):
        print(i)
        one_round(player1, player2)
    print(player1.win_count)
    print(player2.win_count)

# test()
# def main():
    # WIN = pygame.display.set_mode((WIDTH * 2 + 2 * SQUARE_SIZE, HEIGHT))
    # player1 = randomPlayer(WHITE)
    # player2 = randomPlayer(BLACK)
    # for i in range(5):
    #     print(i)
    #     one_round(WIN,player1, player2)
    # print(player1.win_count)
    # print(player2.win_count)
#     boards=Boards()
#     gs=GameState(WHITE,boards)
#     gs.boards.board1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#                  [1, 0, 0, 0, 0, Piece(1, 5, WHITE, 1), 0, 0, 0, 1],
#                  [1, 0, 0, 0, Piece(2, 4, BLACK, 1), 0, Piece(2, 6, BLACK, 1), 0, 0, 1],
#                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                  [1, 0, Piece(4, 2, BLACK, 1), 0, 0, 0, 0, 0, 0, 1],
#                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                  [1, 0, 0, 0, 0, Piece(6, 5, WHITE, 1), 0, 0, 0, 1],
#                  [1, 0, Piece(7, 2, BLACK, 1), 0, Piece(7, 4, BLACK, 1), 0, 0, 0, 0, 1],
#                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
#
#     for m in gs.boards.board1:
#         print(m)
#     next_moves = gs.get_valid_moves()
#     for i in next_moves:
#         print(i)
# main()
def main():
    run=True
    boards=Boards()
    clock = pygame.time.Clock()
    WIN= pygame.display.set_mode((WIDTH*2+2*SQUARE_SIZE, HEIGHT))
    random = False
    mx=True #ax
    cvc=False#final
    gs = GameState(BLACK, boards, 0)
    player = humanPlayer(WIN, gs)
    mxplayer1=MinimaxPlayer(WHITE,'capture',1)
    mxplayer2 = MinimaxPlayer(BLACK, 'capture', 1)
    rdplayer=randomPlayer(WHITE)
    rdplayer1 = randomPlayer(BLACK)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
             if event.type==pygame.QUIT:
                 run=False
        if mx:
            if  player.gs.player == WHITE:
                next_move = mxplayer1.get_next_move(player.gs,player)
                player.ai_move(next_move)

        if cvc:
            if  player.gs.player == WHITE:
                next_move = mxplayer1.get_next_move(player.gs,player)
                player.ai_move(next_move)

            if player.gs.player == BLACK:
                next_move = rdplayer1.get_next_move(player.gs)
                player.ai_move(next_move)

        if random:
            if  player.gs.player == WHITE:
                next_move = rdplayer.get_next_move(player.gs)
                player.ai_move(next_move)

        if not cvc:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col,board_num = get_row_col_from_mouse(pos)
                player.select(row, col,board_num)
                boards.draw_board(WIN)

        player.update_win()
    pygame.quit()
main()


# gs = GameState(WHITE, boards)
# # one_round(player1, player0)
# stats = {}
#
# for i in range(3):
#     one_round(player1, player0)
#     stats[i] = {"tag1": player1.player_tag, "win1": player1.win_count, "tag2": player2.player_tag,
#                 "win2": player2.win_count}
# print(player1.win_count)
# print(player2.win_count)
# print(stats)
