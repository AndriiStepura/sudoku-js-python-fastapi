from board_mocks import mock1, mock2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
# https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock1' - 200 and mockId1 with first sudoku body
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock2' - 200 and mockId2 with second sudoku body
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock3' - 404

#TODO for next app versions apply structure with routers
# https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure



class GridValidation(BaseModel):
    gridId: str
    grid: list
    errors: list | None = None # No errors expected in req but we want to return them in resp

@app.post("/verifygrid/")
async def grid_validation(request: GridValidation):    
    response = request
    responseErrors = ["fix a1"] #TODO put here  actual grid (game board) validation result
    response.errors = responseErrors
    return response