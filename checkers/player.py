import random


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

class MinimaxPlayer:

    def __init__(self, piece, ai=False, strategy=0):
        self.piece = piece
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0

    def minimax_moves(self, next_move_options):
        pass