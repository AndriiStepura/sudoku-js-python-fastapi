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
    errorCells: list[wrongCell]  # List of problematic cells
    errorsMessage: str | None  # Main error message sting for UI


# Verify grid
def verify_grid(gridId, grid):
    verifyGrifResults = ResponseVerifyGrid(
        gridId=gridId, grid=grid, errorCells=[], errorsMessage=None
    )

    # verifyGrifResults.gridId = gridId # no need for modifications for gridId

    # TODO add here def verify_cheating function to throw unexpected data change error
    # If post grid with try to overwright changeable=False base cells - throw Critical allert back
    # error1 = wrongCell(x=0,y=2,cellErrorMessage="Cheating")
    # verifyGrifResults.errorCells.append(error1)
    # verifyGrifResults.errorsMessage = "No cheating! You cannot change the starting grid values."

    # if error returned propagate it through errorsMessage response property
    originalNonChangeableGridCells = grid
    # and TODO return mapped with original changeable=False in case if front-end miss this protection to avoid cheating
    verifyGrifResults.grid = originalNonChangeableGridCells

    # TODO add here def verify_vertical_lines function to return duplicates after vertical lines check
    # And add them to errorCells list
    # error2 = wrongCell(x=*,y=0,cellErrorMessage="Vertical row duplicate")
    # verifyGrifResults.errorCells.append(error2)
    # verifyGrifResults.errorsMessage = "Numbers should not be repeated in a vertical row."

    # TODO add here def verify_horisontal_lines function to return duplicates after horisontal lines check
    # And add them to errorCells list
    # error3 = wrongCell(x=0,y=*,cellErrorMessage="Horisontal row duplicate")
    # verifyGrifResults.errorCells.append(error3)
    # verifyGrifResults.errorsMessage = "Numbers should not be repeated in a horizontal row."

    # TODO add here def verify_regions function to return duplicates after regions check
    # And add them to errorCells list
    # error4 = wrongCell(x=n*3,y=n*3,cellErrorMessage="Regional block duplicate")
    # verifyGrifResults.errorCells.append(error4)
    # verifyGrifResults.errorsMessage = "Numbers should not be repeated in region block."

    # TODO add here def verify_empty_cells function to return info about not populated cells
    # And add them to errorCells list
    # error4 = wrongCell(x=any,y=any,cellErrorMessage="Missed value")
    # verifyGrifResults.errorCells.append(error4)
    # verifyGrifResults.errorsMessage = "To finish sudoky all cells should be populated with valuse 1-9"

    return verifyGrifResults
