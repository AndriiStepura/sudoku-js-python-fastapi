from pydantic import BaseModel
from typing import List, Dict, Any
from board import BoardCell
from board_mocks import mock1, mock2, convert_board


class wrongCell(BaseModel):
    x: int
    y: int
    cellErrorsMessages: List[str]


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
    
    verifyGridResults = verify_vertical_duplicates(verifyGridResults)
    
    verifyGridResults = verify_horisontal_duplicates(verifyGridResults)
    
    # verifyGridResults.errorsMessages = "Numbers should not be repeated in a horizontal row."

    # TODO add here def verify_regions function to return duplicates after regions check
    # And add them to errorCells list
    # error4 = wrongCell(x=n*3,y=n*3,cellErrorsMessages="Regional block duplicate")
    # verifyGridResults.errorCells.append(error4)
    # verifyGridResults.errorsMessages = "Numbers should not be repeated in region block."

    # TODO add here def verify_empty_cells function to return info about not populated cells
    # And add them to errorCells list
    # error4 = wrongCell(x=any,y=any,cellErrorsMessages="Missed value")
    # verifyGridResults.errorCells.append(error4)
    # verifyGridResults.errorsMessages = "To finish sudoky all cells should be populated with valuse 1-9"

    verifyGridResults.errorCells = merge_error_cells_records(verifyGridResults.errorCells)

    return verifyGridResults


def verify_cheating_helper(verifyGridResultsIn: ResponseVerifyGrid):
    verifyGridResultsAfterCheatingCheck = verifyGridResultsIn

    # Get original grid
    mocks = {"mock1": mock1, "mock2": mock2}
    originalGrid = mocks.get(verifyGridResultsIn.gridId)

    verifyGridResultsAfterCheatingCheck = cheating_helper_iterator(
        originalGrid, verifyGridResultsAfterCheatingCheck
    )
    if len(verifyGridResultsAfterCheatingCheck.errorCells) > 0:
        verifyGridResultsAfterCheatingCheck.errorsMessages.append(
            "No cheating! You cannot change the starting grid values."
        )

    return verifyGridResultsAfterCheatingCheck


def cheating_helper_iterator(
    original: List[BoardCell], verifyCheatinglIn: ResponseVerifyGrid
) -> List[wrongCell]:

    fromUserAsABoard = List[BoardCell]
    fromUserAsABoard = convert_board(verifyCheatinglIn.grid)

    # Compare cell by cell to verify same value for non changeble cells)
    for original_cell, user_cell in zip(original, fromUserAsABoard):
        if not original_cell.changeable:
            if original_cell.value != user_cell.value:
                # Report
                verifyCheatinglIn.errorCells.append(
                    wrongCell(
                        x=original_cell.x,
                        y=original_cell.y,
                        cellErrorsMessages=["Cheating"],
                    )
                )
                # Overwrite value back
                (verifyCheatinglIn.grid[original_cell.x])[original_cell.y] = original_cell.value
    return verifyCheatinglIn


def verify_vertical_duplicates(verifyVerticalIn: ResponseVerifyGrid):
    board = verifyVerticalIn.grid
    generalErrorMessageAdded = False
    for col in range(len(board)):
        seen = {} #to store known values
        for row in range(len(board[col])):
            val = board[row][col]
            if val == 0:
                continue # ignore empty cells
            # if value seen before the duplicate found
            if val in seen:
                if generalErrorMessageAdded != True:
                    verifyVerticalIn.errorsMessages.append("Numbers should not be repeated in a vertical row.")
                    generalErrorMessageAdded = True

                # append both current and the one already seen
                verifyVerticalIn.errorCells.append(wrongCell(x=col, y=row, cellErrorsMessages=["Vertical row duplicate"]))

                # add previous occurrences (if not already added)
                if not any(e.x == seen[val] and e.y == col for e in verifyVerticalIn.errorCells):
                    verifyVerticalIn.errorCells.append(wrongCell(x=col, y=seen[val], cellErrorsMessages=["Vertical row duplicate"]))
            else:
                seen[val] = row

    return verifyVerticalIn


def verify_horisontal_duplicates(verifyVerticalIn: ResponseVerifyGrid):
    board = verifyVerticalIn.grid
    generalErrorMessageAdded = False
    for row in range(len(board)):
        seen = {} #to store known values
        for col in range(len(board[row])):
            val = board[row][col]
            if val == 0:
                continue # ignore empty cells
            # if value seen before the duplicate found
            if val in seen:
                if generalErrorMessageAdded != True:
                    verifyVerticalIn.errorsMessages.append("Numbers should not be repeated in a horizontal row.")
                    generalErrorMessageAdded = True

                # append both current and the one already seen
                verifyVerticalIn.errorCells.append(wrongCell(x=col, y=row, cellErrorsMessages=["Horisontal row duplicate"]))
                
                # add previous occurrences (if not already added)
                if not any(e.x == row and e.y == seen[val] for e in verifyVerticalIn.errorCells):
                    verifyVerticalIn.errorCells.append(wrongCell(x=seen[val], y=row, cellErrorsMessages=["Horisontal row duplicate"]))
            else:
                seen[val] = col

    return verifyVerticalIn


# Merge error messages for same cell, it should simplify UI mapping
def merge_error_cells_records(wrongCellsList: List[Dict[str, Any]]) -> List[wrongCell]:   
    merged = {}
    for cell in wrongCellsList:
        key = (cell.x, cell.y)

        error = cell.cellErrorsMessages
        if isinstance(error, str):
            erroerrorrerrors = [error]

        if key not in merged:
            merged[key] = wrongCell(x=cell.x, y=cell.y, cellErrorsMessages=list(set(error)))
        else:
            merged[key].cellErrorsMessages = list(set(merged[key].cellErrorsMessages + error))

    return list(merged.values())
