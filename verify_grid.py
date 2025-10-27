from pydantic import BaseModel
class wrongCell(BaseModel):
    x: int 
    y: int
    cellErrorMessage: str = None

class RequestVerifyGrid(BaseModel):
    gridId: str
    grid: list

class ResponseVerifyGrid(BaseModel):
    gridId: str
    grid: list
    errorCells: list[wrongCell] # List of problematic cells
    errorsMessage: str | None # Main error message sting for UI
    
# Verify grid
def verify_grid(gridId, grid):   
    verifyGrifResults = ResponseVerifyGrid(gridId=gridId, grid=grid, errorCells=[], errorsMessage=None)
    originalNonChangeableGridCells = grid
    verifyGrifResults.grid = originalNonChangeableGridCells


    validationResults.errorsMessage = "You can't change starting grid values"

    return verifyGrifResults
