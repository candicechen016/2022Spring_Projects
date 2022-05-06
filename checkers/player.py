"""
Player module
"""

import random
from copy import deepcopy

from checkers.cons import WHITE, BLACK


class randomPlayer:
    def __init__(self, color):
        self.player_tag = 'Random'
        self.win_count = 0
        self.color = color

    def get_next_move(self, gamestate):
        next_move_options = gamestate.get_valid_moves()
        mode1_num = len(next_move_options['one_move'])
        mode2_num = len(next_move_options['two_move'])
        mode3_num = len(next_move_options['transfer_move'])
        option_list = [1] * mode1_num + [2] * mode2_num + [3] * mode3_num
        next_move = []
        # next_move_mode = 0
        if option_list:
            next_move_mode = random.choice(option_list)
            if next_move_mode == 1:
                next_move = random.choice(next_move_options['one_move'])
            elif next_move_mode == 2:
                next_move = random.choice(next_move_options['two_move'])
            elif next_move_mode == 3:
                next_move = random.choice(next_move_options['transfer_move'])
        return next_move


class MinimaxPlayer:

    def __init__(self, color, strategy, depth):
        self.player_tag = 'Minimax_{}_d{}'.format(strategy, depth)
        self.color = color
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0
        self.strategy = strategy  # 'kings' or 'capture'
        self.depth = depth

    def get_next_move(self, gamestate):
        next_move_options = gamestate.get_all_valid_moves()
        best_move = None
        highest_score = float('-inf')
        if next_move_options:
            for idx, next_move in enumerate(next_move_options):
                gamestate.reset()
                next_gamestate = simulate_move(gamestate, next_move)
                node_score = self.minimax_moves(gamestate=next_gamestate, max_player=True, depth=self.depth)
                if node_score > highest_score:
                    highest_score = node_score
                    best_move = next_move
        print("best_move", best_move)
        return best_move

    def minimax_moves(self, gamestate, max_player, depth):
        """
        O(n^m), n: number of nodes, m:depth

        Minimax pseudocode was referred from:
        https://www.youtube.com/watch?v=l-hh51ncgDI&t=254s
        """
        next_move_options = gamestate.get_all_valid_moves()
        gamestate.player = WHITE if gamestate.player == BLACK else BLACK
        gamestate.opponent = WHITE if gamestate.opponent == BLACK else BLACK
        if next_move_options == [] or depth == 0 or gamestate.game_over():
            return gamestate.evaluation(self.strategy, next_move_options)
        if max_player:
            max_value = float('-inf')
            # loop each child
            for next_move_info in next_move_options:
                # generate new gamestate
                next_gamestate = simulate_move(gamestate, next_move_info)
                # evaluation
                value = self.minimax_moves(gamestate=next_gamestate, max_player=False, depth=depth - 1)
                print("compare", "max_value", max_value, "value", value)
                max_value = max(max_value, value)

            print("max_value", max_value)
            return max_value
        else:
            print("min_player")
            min_value = float('inf')
            for next_move_info in next_move_options:
                print("next_move_info:", next_move_info)
                next_gamestate = simulate_move(gamestate, next_move_info)
                value = self.minimax_moves(gamestate=next_gamestate, max_player=True, depth=depth - 1)
                print("compare", "min_value", min_value, "value", value)
                min_value = min(min_value, value)
            print("final min_value", min_value)
            return min_value


def simulate_move(game, next_move):
    """
    O(n)

    """
    simulated_game = deepcopy(game)
    for move in next_move:  # O(n)

        if move['start_board'] != move['end_board']:
            simulated_game.transfer_piece(move, make_move=True)
        else:
            if move['start_board'] == 1:
                simulated_game.update_board_normal(move, simulated_game.boards.board1, make_move=True)
            else:
                simulated_game.update_board_normal(move, simulated_game.boards.board2, make_move=True)

    return simulated_game
