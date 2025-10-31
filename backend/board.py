# Default board cell object
class BoardCell(object):
    x = 0
    y = 0
    changeable = True
    value = None

    def __init__(self, x, y, changeable, value):
        self.x = x
        self.y = y
        self.changeable = changeable
        self.value = value


# For default empty cell:
#    make_boardCell(0,0)
# For blocked to change cell with values:
#    make_boardCell(0,0,False,5)
def make_boardCell(x, y, changeable=True, value=None):
    cell = BoardCell(x, y, changeable, value)
    return cell


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
