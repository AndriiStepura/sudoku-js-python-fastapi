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
  
a1 = make_boardCell(1,1)
a2 = make_boardCell(1,2,False,"5")
# Print for debug result in a JSON:
#print(a1.toJSON())
#print(a2.toJSON())


@app.get("/")
def root():
    return {"Hello": "I'm sudoku back-end with python FastAPI"}
mock1 = []
a1 = make_boardCell(1,1)
a2 = make_boardCell(1,2,False,5)
mock1.append(a1)
mock1.append(a2)


# Print for debug result in a JSON:
# print(a1.toJSON())
# print(a2.toJSON())

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