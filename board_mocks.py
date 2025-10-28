from board import make_boardCell


# Helper to create board from array of ints
def convert_board(board):
    board_objects = []
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                board_objects.append(make_boardCell(i, j, True))
            else:
                board_objects.append(make_boardCell(i, j, False, val))
    return board_objects


# mock1
mock1 = convert_board(
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
)

# mock2
mock2 = convert_board(
    [
        [0, 0, 0, 2, 1, 0, 0, 0, 0],
        [0, 0, 7, 3, 0, 0, 0, 0, 0],
        [0, 5, 8, 0, 0, 0, 0, 0, 0],
        [4, 3, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 7, 6, 0],
        [0, 0, 0, 0, 2, 5, 0, 0, 0],
        [0, 0, 0, 7, 3, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 0, 0],
    ]
)
