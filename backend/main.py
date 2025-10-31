from board_mocks import mock1, mock2
from verify_grid import verify_grid, RequestVerifyGrid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
apiVersion = "v1"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder to serve HTML/JS/CSS
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


@app.get("/")
def serve_frontend():
    """Serve the main HTML page."""
    return FileResponse("../frontend/index.html")


@app.get("/{apiVersion}/")
def root():
    return {
        "message": "I'm sudoku back-end with python FastAPI you can call to GET /newgrid to receive new sudoku game board or POST /verifygrid to validate your puzzle",
        "errors": None,
    }


# Endpoint to get new game board
@app.get("/{apiVersion}/newgrid")
def get_newgrid(gridId: str = "mock1"):
    gridInResponse = []
    responseErrors = []

    mocks = {"mock1": mock1, "mock2": mock2}
    gridInResponse = mocks.get(gridId)

    if not gridInResponse:
        responseErrors.append(f"gridId {gridId} NOT FOUND")

    if len(responseErrors) == 0:
        return {"gridId": gridId, "grid": gridInResponse}
    else:
        # https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception
        raise HTTPException(status_code=404, detail=responseErrors)


# TODO add Int tests
# https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock1' - 200 and mockId1 with first sudoku body
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock2' - 200 and mockId2 with second sudoku body
# curl --location 'http://127.0.0.1:8000/newgrid?gridId=mock3' - 404

# TODO for next app versions apply structure with routers
# https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure


@app.post("/{apiVersion}/verifygrid/")
async def post_verifygrid(request: RequestVerifyGrid):
    # TODO move error strings to common util for DRY
    responseValidationResult = verify_grid(request.gridId, request.grid)
    return responseValidationResult
