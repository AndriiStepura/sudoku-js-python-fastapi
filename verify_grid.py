from pydantic import BaseModel

class wrongCell(BaseModel):
    x: int 
    y: int
    cellErrorMessage: str = None

class validationResult(BaseModel):
    errorCells: list[wrongCell]  = None
    errorsMessage: str = None
    

# Verify grid
def verify_grid(gridId, grid):            
    validationResults = validationResult()    

    validationResults.errorCells = []
    error1 = wrongCell(x=0,y=2,cellErrorMessage="Cheating")
    error2 = wrongCell(x=1,y=1,cellErrorMessage="Duplicate")
    validationResults.errorCells.append(error1)
    validationResults.errorCells.append(error2)

    validationResults.errorsMessage = "You can't change starting grid values"

    return validationResults
