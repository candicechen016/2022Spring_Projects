"""
Player module: Random Player and Minimax Player
"""

import random
from copy import deepcopy

from checkers.cons import WHITE, BLACK, ROWS


class randomPlayer:
    def __init__(self, color):
        self.player_tag = 'Random'
        self.win_count = 0
        self.color = color

    def get_next_move(self, game):
        next_move_options = game.gs.get_valid_moves()
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
                game.gs.boards.transfer_count[self.color] += 1
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
        self.count_transfer = 0
        half_edge = ROWS // 2
        self.center_square = [(half_edge, half_edge), (half_edge + 1, half_edge), (half_edge, half_edge + 1),
                              (half_edge + 1, half_edge + 1)]

    def get_next_move(self, game):
        next_move_options = game.gs.get_all_valid_moves()
        print("next_move_options", len(next_move_options))
        print("next_move_options", next_move_options[0])
        top_candidates = []
        second_candidates = []
        third_candidates = []
        minimax_candidates = []
        best_move = None

        for next_move in next_move_options:
            if next_move[0]['end_move'] in self.center_square or next_move[1]['end_move'] in self.center_square:
                top_candidates.append(next_move)
            if next_move[0]['capture'] or next_move[1]['capture']:
                second_candidates.append(next_move)
            if next_move[0]['start_move'] != next_move[1]['start_move']:
                third_candidates.append(next_move)

        if top_candidates:
            best_move = random.choice(top_candidates)
        elif second_candidates:
            minimax_candidates += second_candidates
            best_move = random.choice(second_candidates)
        else:
            minimax_candidates += next_move_options
            best_move = random.choice(third_candidates)

        if game.turn_num // 2 <= ROWS * 2:
            return best_move

        highest_score = float('-inf')

        for next_move in minimax_candidates:
            game.gs.reset()
            next_gamestate = simulate_move(game.gs, next_move)
            node_score = self.minimax_moves(alpha=float("-inf"), beta=float("+inf"), gamestate=next_gamestate,
                                            max_player=True, depth=self.depth)
            if node_score > highest_score:
                highest_score = node_score
                best_move = next_move
        if best_move[0]['start_board'] != best_move[0]['end_board']:
            game.gs.boards.transfer_count[self.color] += 1
        return best_move

    def minimax_moves(self, alpha, beta, gamestate, max_player, depth):
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
                value = self.minimax_moves(alpha, beta, gamestate=next_gamestate, max_player=False, depth=depth - 1)
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return max_value
        else:
            min_value = float('inf')
            for next_move_info in next_move_options:
                next_gamestate = simulate_move(gamestate, next_move_info)
                value = self.minimax_moves(alpha, beta, gamestate=next_gamestate, max_player=True, depth=depth - 1)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
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
