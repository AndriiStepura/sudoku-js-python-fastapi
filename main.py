from board_mocks import mock1
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "I'm sudoku back-end with python FastAPI you can call to GET /newgrid to receive new sudoku game board or POST /verifygrid to validate your puzzle",
        "errors": None
        }

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