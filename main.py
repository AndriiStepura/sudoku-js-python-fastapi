from fastapi import FastAPI

app = FastAPI()

#Default board cell object
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


@app.get("/")
def root():
    return {
        "message": "I'm sudoku back-end with python FastAPI you can call to GET /newgrid to receive new sudoku game board or POST /verifygrid to validate your puzzle",
        "errors": None
        }


#mock1
mock1 = []
mock1_as_ints=[
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

mock1 = convert_board(mock1_as_ints)
# a1 = make_boardCell(1,1)
# a2 = make_boardCell(1,2,False,5)
# mock1.append(a1)
# mock1.append(a2)

# Print for debug result in a JSON:
# print(mock1)

# Endpoint to get new game board
@app.get("/newgrid")
def root():
    return {
            "gridId": "mock1",
            "grid": [
                     mock1
                    ],
            "errors": None
        }