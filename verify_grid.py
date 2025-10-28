from pydantic import BaseModel
from typing import List
from board import BoardCell
from board_mocks import mock1, mock2, convert_board


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
    errorsMessages: list  # Main errors message stings for UI


# Verify grid
def verify_grid(gridId, grid):
    verifyGridResults = ResponseVerifyGrid(
        gridId=gridId, grid=grid, errorCells=[], errorsMessages=[]
    )

    # verifyGridResults.gridId = gridId # no need for modifications for gridId

    # If post grid with try to overwright changeable=False base cells - throw Critical allert back
    verifyGridResults = verify_cheating_helper(verifyGridResults)

    # if error returned propagate it through errorsMessages response property
    originalNonChangeableGridCells = grid
    # and TODO return mapped with original changeable=False in case if front-end miss this protection to avoid cheating
    verifyGridResults.grid = originalNonChangeableGridCells

    # TODO add here def verify_vertical_lines function to return duplicates after vertical lines check
    # And add them to errorCells list
    # error2 = wrongCell(x=*,y=0,cellErrorMessage="Vertical row duplicate")
    # verifyGridResults.errorCells.append(error2)
    # verifyGridResults.errorsMessages = "Numbers should not be repeated in a vertical row."

    # TODO add here def verify_horisontal_lines function to return duplicates after horisontal lines check
    # And add them to errorCells list
    # error3 = wrongCell(x=0,y=*,cellErrorMessage="Horisontal row duplicate")
    # verifyGridResults.errorCells.append(error3)
    # verifyGridResults.errorsMessages = "Numbers should not be repeated in a horizontal row."

    # TODO add here def verify_regions function to return duplicates after regions check
    # And add them to errorCells list
    # error4 = wrongCell(x=n*3,y=n*3,cellErrorMessage="Regional block duplicate")
    # verifyGridResults.errorCells.append(error4)
    # verifyGridResults.errorsMessages = "Numbers should not be repeated in region block."

    # TODO add here def verify_empty_cells function to return info about not populated cells
    # And add them to errorCells list
    # error4 = wrongCell(x=any,y=any,cellErrorMessage="Missed value")
    # verifyGridResults.errorCells.append(error4)
    # verifyGridResults.errorsMessages = "To finish sudoky all cells should be populated with valuse 1-9"

    return verifyGridResults


def verify_cheating_helper(verifyGridResultsIn: ResponseVerifyGrid):
    verifyGridResultsAfterCheatingCheck = verifyGridResultsIn

    # Get original grid
    mocks = {"mock1": mock1, "mock2": mock2}
    originalGrid = mocks.get(verifyGridResultsIn.gridId)

    verifyGridResultsAfterCheatingCheck.errorCells = cheating_helper_iterator(
        originalGrid, verifyGridResultsIn.grid
    )

    # Simulate wrong cell
    # verifyGridResultsAfterCheatingCheck.errorCells.append(
    #     wrongCell(x=0, y=0, cellErrorMessage="Cheating")
    # )
    # verifyGridResultsAfterCheatingCheck.errorCells.append(
    #     wrongCell(x=3, y=4, cellErrorMessage="Cheating")
    # )
    # verifyGridResultsAfterCheatingCheck.errorsMessages.append(
    #     "No cheating! You cannot change the starting grid values."
    # )
    return verifyGridResultsAfterCheatingCheck


def cheating_helper_iterator(
    original: List[BoardCell], fromUser: List[BoardCell]
) -> List[wrongCell]:
    wrong_cells = []
    fromUserAsABoard = List[BoardCell]
    fromUserAsABoard = convert_board(fromUser)
    
    # Compare cell by cell to verify same value for non changeble cells)
    for original_cell, user_cell in zip(original, fromUserAsABoard):
        if not original_cell.changeable:
            if original_cell.value != user_cell.value:
                # Overwrite back
                user_cell.value = original_cell.value
                wrong_cells.append(
                    wrongCell(
                        x=original_cell.x,
                        y=original_cell.y,
                        cellErrorMessage="Cheating"
                    )
                )
    return wrong_cells
