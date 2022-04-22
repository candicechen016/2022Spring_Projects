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
        self.board1 = [['w1', '.', 'w1', '.'],
                      ['.', 'w1', '', 'w1'],
                      ['b1', '.', 'b1', '.'],
                      ['.', 'b1', '.','b1']]  # numpy array 6x6

        self.board2 = [['.', 'w2', '.', 'w2'],
                       ['.', '.', '.', '.'],
                       ['.', '.', '.', '.'],
                       ['.', '.', '.', '.']]  # np.argwhere(self.pstate==player)

        self.placed_positions = {    # to store moves
            w1: np.array([(0,0)]),
            w2: None,
            b1:None,
            b2:None}




    def capture(self):

    def check_win(self):




    def make_move(self):


    def get_move_list(self):
        """get valid moves, i.e. empty squares"""


    def update_board(self):




class Piece:

    def __int__(self):
        self.color = []


    """
    This class is used to initialise the board, check the winning conditions and check if the move
    played by user is a valid move
    """
    def __init__(self):
        self.board = [['.', '.', '.', '.'],
                      ['.', '.', '.', '.'],
                      ['.', '.', '.', '.'],
                      ['.', '.', '.', '.']]

    def get_board_str(self):
        return str(self.board)

    def get_board(self):
        return self.board

    def __str__(self):
        return '\n'.join(map(' '.join, self.board))

    def valid_move(self, move):
        x, y = move[0], move[1]
        if 0 <= x <= 3 and 0 <= y <= 3 and self.board[x][y] == '.':
            return True
        return False

    def draw(self):
        return all(all(x != '.' for x in y) for y in self.board)

    def winning(self):
        board = np.array(self.board)
        if board[0, 0] != '.' and (board[0, 0] == board[0, 3] == board[3, 0] == board[3, 3]):
            return True

        if any([True if (board[i, 0] != '.' and (board[i, 0] == board[i, 1] == board[i, 2] == board[i, 3]))
                else False for i in range(0, 4)]):
            return True

        if any([True if (board[0, j] != '.' and (board[0, j] == board[1, j] == board[2, j] == board[3, j]))
                else False for j in range(0, 4)]):
            return True
        for row in range(0, 3):
            for col in range(0, 3):
                if board[row, col] != '.' and \
                        (board[row, col] == board[row + 1, col] == board[row, col + 1] == board[row + 1, col + 1]):
                    return True

        if board[0, 0] != '.' and board[0, 0] == board[1, 1] == board[2, 2] == board[3, 3]:
            return True
        if board[0, 3] != '.' and board[0, 3] == board[1, 2] == board[2, 1] == board[3, 0]:
            return True

        return False

    def play_move(self, position, marker):
        self.board[position[0]][position[1]] = marker


class RandomPlayer:
    """
    This class represents the RandomPlayer where the player moves are generated randomly
    """
    def __init__(self, player):
        self.player = player
        self.win_count = 0
        self.draw_count = 0
        self.lose_count = 0

    def get_move(self, board):
        while True:
            move = (random.randrange(4), random.randrange(4))
            if board.valid_move(move):
                break
        return move

    def start_game(self):
        pass

    def win_game(self):
        self.win_count = self.win_count + 1
        return f"Player {self.player} won!"

    def lose_game(self):
        self.lose_count = self.lose_count + 1
        return f"Player {self.player} lost!"

    def draw_game(self):
        self.draw_count = self.draw_count + 1
        return f"It's a draw"

    def return_count(self):
        print(f"Random Winning counts, Win: {self.win_count}, Draw: {self.draw_count}, Lose: {self.lose_count}")


class MenacePlayer:
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
    player1 = MenacePlayer(1)
    player2 = RandomPlayer(2)
    for i in range(1, 1000):
        play_game(player1, player2)
    player1.return_count()
    player2.return_count()



