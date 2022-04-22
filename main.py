"""
Parallel-Universes Checkers.

winninig:
1. NO PIECES on both boards
2. NO STEPS AND NO TRANFE on both boards

rules:
1. can only Transfer once
2. can not capture at the transferring round
3. only transfer to an empty square and must go to an orthogonally-adjacent square
4. Make Moves:
    a. move one piece at the same universe two turns
    b. move one piece of each board

"""

import numpy as np
import random


class GameState:
    def __init__(self):
        self.board1 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 'w1', '.', 'w1', '.', 'w1', '.', 1],
                                [1, '.', 'w1', '.', 'w1', '.', 'w1', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, 'b1', '.', 'b1', '.', 'b1', '.', 1],
                                [1, '.', 'b1', '.', 'b1', '.', 'b1', 1],
                                [1, 1, 1, 1, 1, 1, 1, 1]])

        self.board2 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                [1, '.', 'w2', '.', 'w2', '.', 'w2', 1],
                                [1, 'w2', '.', 'w2', '.', 'w2', '.', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, '.', '.', '.', '.', '.', '.', 1],
                                [1, '.', 'b2', '.', 'b2', '.', 'b2', 1],
                                [1, 'b2', '.', 'b2', '.', 'b2', '.', 1],
                                [1, 1, 1, 1, 1, 1, 1, 1]])

    def find_orthogonally_neighbors(self, piece, piece_position, board):
        x, y = piece_position
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        empty = []
        for n in neighbors:
            #     print(n)
            # if size in n or -1 in n:
            #     continue
            # else:
            if board[n] == '.':
                empty.append(n)
        print(empty)
        return empty

    def check_win(self, player):
        boards = [self.board1, self.board2 ]
        all_valid = []
        for board in boards.values():
            for piece in player:
                piece_positions = np.argwhere(board == piece)
                # condition 1: the player has NO PIECES on Both boards
                if piece_positions.size == 0:
                    continue
                else:
                    # condition 2: the player has NO STEPS AND NO way to transfer on both boards

                    for position in piece_positions:
                        valid_transfer_squares = self.find_orthogonally_neighbors(piece, position, board)
                        all_valid += valid_transfer_squares
        if not all_valid:
            return True
        # else:
        #     for position in valid_transfer_squares:
        #         # TODO: call make move function and get the boards
        else:
            return False



    def make_move(self):



    def capture(self):










class RandomPlayer:
    """
    This class represents the RandomPlayer where the player moves are generated randomly
    """

    def __init__(self, player):
        self.player = player
        self.win_count = 0
        self.draw_count = 0
        self.lose_count = 0


class AIPlayer:
    """
    This class represents the Menace player , it contains a function which keeps track of all the win and lost moves of
    the player in a dictionary.
    """

    def __init__(self, player):
        self.player = player
        self.matchbox_dict = {}
        self.beads = []
        self.win_count = 0
        self.draw_count = 0
        self.lose_count = 0

    def start_game(self):
        self.move_list = []

    def get_move(self, board):
        for i in range(0, 1):
            board_state_str = board.get_board_str()
            board_state = board.get_board()
            if board_state_str not in self.matchbox_dict:
                for row in range(0, 4):
                    for col in range(0, 4):
                        if board_state[row][col] == '.':
                            self.beads.append((row, col))
                            self.beads.append((row, col))
                self.matchbox_dict[board_state_str] = self.beads
            list_beads = self.matchbox_dict[board_state_str]
            list_bead_random_choice = random.choice(list_beads)
            if board.valid_move(list_bead_random_choice):
                self.move_list.append((board_state_str, list_bead_random_choice))

            return list_bead_random_choice

    def win_game(self):
        self.win_count = self.win_count + 1
        for move in self.move_list:
            self.matchbox_dict[move[0]].extend([move[1], move[1], move[1]])
        return f"Player {self.player} won!"

    def lose_game(self):
        self.lose_count = self.lose_count + 1
        for move in self.move_list:
            list(filter((move[1]).__ne__, self.matchbox_dict[move[0]]))
        return f"Player {self.player} lost!"

    def draw_game(self):
        self.draw_count = self.draw_count + 1
        return f"It's a draw"

    def return_count(self):
        print(f"Menace Winning counts, Win: {self.win_count}, Draw: {self.draw_count}, Lose: {self.lose_count}")


def play_game(first, second):
    board = Board()
    first.start_game()
    second.start_game()
    while True:
        move = first.get_move(board)
        board.play_move(move, 'X')
        if board.winning():
            first.win_game()
            second.lose_game()
            break
        if board.draw():
            first.draw_game()
            second.draw_game()
            break

        move = second.get_move(board)
        board.play_move(move, 'O')
        if board.winning():
            first.lose_game()
            second.win_game()
            break
        if board.draw():
            first.draw_game()
            second.draw_game()
            break


if __name__ == '__main__':
    # player1 = MenacePlayer(1)
    player2 = RandomPlayer(2)
    # for i in range(1, 1000):
    #     play_game(player1, player2)
    # player1.return_count()
    player2.return_count()
