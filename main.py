import json
from fastapi import FastAPI

app = FastAPI()

#Default board cell object
class BoardCell(object):
    x = 0
    y = 0
    changeable = True
    value = ""
        
    def __init__(self, x, y, changeable, value):
        self.x = x
        self.y = y        
        self.changeable = changeable
        self.value = value

    # workaround for serialisation by https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=False,
            indent=4)

def make_boardCell(x, y, changeable=True, value=""):
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

# Endpoint to get new game board
@app.get("/newgrid")
def root():
    return {
            "gridId": "mock1",
            "grid": [
                     json.loads(a1.toJSON()),
                     json.loads(a2.toJSON())
                    ],
            "error": None
        }