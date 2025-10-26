from board_mocks import mock1, mock2
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "I'm sudoku back-end with python FastAPI you can call to GET /newgrid to receive new sudoku game board or POST /verifygrid to validate your puzzle",
        "errors": None
        }

# Endpoint to get new game board
@app.get("/newgrid")
def new_grid(gridId:str="mock1"):
    gridInResponse = []
    responseErrors = []

    mocks = {
        "mock1": mock1,
        "mock2": mock2
    }

    gridInResponse = mocks.get(gridId)
    if not gridInResponse:
        responseErrors.append(f"gridId {gridId} NOT FOUND")

    if len(responseErrors) == 0:
        return {
                "gridId": gridId,
                "grid": [
                            gridInResponse
                        ],
                "errors": responseErrors
            }
    else:
        # https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception
        raise HTTPException(status_code=404, detail=responseErrors)
    

#TODO add Int tests 
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock1' 
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock2'
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock3' - 404 
