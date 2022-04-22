import numpy as np
from scipy import ndimage

# board1 = np.array([['w1', '.', 'w1', '.', 'w1', '.'],
#                    ['.', 'w1', '.', 'w1', '.', 'w1'],
#                    ['.', '.', '.', '.', '.', '.'],
#                    ['.', '.', '.', '.', '.', '.'],
#                    ['b1', '.', 'b1', '.', 'b1', '.'],
#                    ['.', 'b1', '.', 'b1', '.', 'b1']])
#
# board2 = np.array([['.', 'w2', '.', 'w2', '.', 'w2'],
#                    ['w2', '.', 'w2', '.', 'w2', '.'],
#                    ['.', '.', '.', '.', '.', '.'],
#                    ['.', '.', '.', '.', '.', '.'],
#                    ['.', 'b2', '.', 'b2', '.', 'b2'],
#                    ['b2', '.', 'b2', '.', 'b2', '.']])

board1 = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 'w1', '.', 'w1', '.', 'w1', '.', 1],
                   [1, '.', 'w1', '.', 'w1', '.', 'w1', 1],
                   [1, '.', '.', '.', '.', '.', '.', 1],
                   [1, '.', '.', '.', '.', '.', '.', 1],
                   [1, 'b1', '.', 'b1', '.', 'b1', '.', 1],
                   [1, '.', 'b1', '.', 'b1', '.', 'b1', 1],
                   [1, 1, 1, 1, 1, 1, 1, 1]])

board2 = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, '.', 'w2', '.', 'w2', '.', 'w2', 1],
    [1, 'w2', '.', 'w2', '.', 'w2', '.', 1],
    [1, '.', '.', '.', '.', '.', '.', 1],
    [1, '.', '.', '.', '.', '.', '.', 1],
    [1, '.', 'b2', '.', 'b2', '.', 'b2', 1],
    [1, 'b2', '.', 'b2', '.', 'b2', '.', 1],
    [1, 1, 1, 1, 1, 1, 1, 1]])

boards = {'1': board1, '2': board2}
size = 6
occupied = np.argwhere(board1 == 'w1')
print(occupied)

p1 = ['w1', 'w2', 'w1k', 'w2k']
p2 = ['b1', 'b2']
mask = [['.', '.', '.', ],
        ['.', '.', '.'],
        ['.', '.', '.', ]]

print(board1[0 + 1, 0])
print('===')


# orthogonally-adjacent square
def find_orthogonally_neighbors(piece, piece_position, board):
    x, y = piece_position
    p = piece[1]
    if piece[1] == '1':
        p == '2'
    else:
        p == '1'

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

def check_win(player,boards):
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
                    valid_transfer_squares = find_orthogonally_neighbors(piece, position, board)
                    all_valid += valid_transfer_squares
    if not all_valid:
        # return True
        print("Over2")
        return True
    # else:
    #     for position in valid_transfer_squares:
    #         # TODO: call make move function and get the boards
    else:
        print("Not yet end")
        return False


check_win(p2,boards)