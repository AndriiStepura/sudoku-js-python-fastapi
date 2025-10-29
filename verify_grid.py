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

    verifyGridResults = verify_region_duplicates(verifyGridResults)

    verifyGridResults = verify_empty_cells(verifyGridResults)

    verifyGridResults.errorCells = merge_error_cells_records(
        verifyGridResults.errorCells
    )

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
                (verifyCheatinglIn.grid[original_cell.x])[
                    original_cell.y
                ] = original_cell.value
    return verifyCheatinglIn


def verify_vertical_duplicates(verifyVerticalIn: ResponseVerifyGrid):
    board = verifyVerticalIn.grid
    generalErrorMessageAdded = False
    for col in range(len(board)):
        seen = {}  # to store known values
        for row in range(len(board[col])):
            val = board[row][col]
            if val == 0:
                continue  # ignore empty cells
            # if value seen before the duplicate found
            if val in seen:
                if generalErrorMessageAdded != True:
                    verifyVerticalIn.errorsMessages.append(
                        "Numbers should not be repeated in a vertical row."
                    )
                    generalErrorMessageAdded = True

                # append both current and the one already seen
                verifyVerticalIn.errorCells.append(
                    wrongCell(
                        x=col, y=row, cellErrorsMessages=["Vertical row duplicate"]
                    )
                )

                # add previous occurrences (if not already added)
                if not any(
                    e.x == seen[val] and e.y == col for e in verifyVerticalIn.errorCells
                ):
                    verifyVerticalIn.errorCells.append(
                        wrongCell(
                            x=col,
                            y=seen[val],
                            cellErrorsMessages=["Vertical row duplicate"],
                        )
                    )
            else:
                seen[val] = row

    return verifyVerticalIn


def verify_horisontal_duplicates(verifyVerticalIn: ResponseVerifyGrid):
    board = verifyVerticalIn.grid
    generalErrorMessageAdded = False
    for row in range(len(board)):
        seen = {}  # to store known values
        for col in range(len(board[row])):
            val = board[row][col]
            if val == 0:
                continue  # ignore empty cells
            # if value seen before the duplicate found
            if val in seen:
                if generalErrorMessageAdded != True:
                    verifyVerticalIn.errorsMessages.append(
                        "Numbers should not be repeated in a horizontal row."
                    )
                    generalErrorMessageAdded = True

                # append both current and the one already seen
                verifyVerticalIn.errorCells.append(
                    wrongCell(
                        x=col, y=row, cellErrorsMessages=["Horisontal row duplicate"]
                    )
                )

                # add previous occurrences (if not already added)
                if not any(
                    e.x == row and e.y == seen[val] for e in verifyVerticalIn.errorCells
                ):
                    verifyVerticalIn.errorCells.append(
                        wrongCell(
                            x=seen[val],
                            y=row,
                            cellErrorsMessages=["Horisontal row duplicate"],
                        )
                    )
            else:
                seen[val] = col
    return verifyVerticalIn


def verify_region_duplicates(verifyRegionIn: ResponseVerifyGrid):
    board = verifyRegionIn.grid
    generalErrorMessageAdded = False
    for box_row in range(0, len(board), 3):
        for box_col in range(0, len(board[box_row]), 3):
            seen = {}
            for i in range(3):
                for j in range(3):
                    row, col = box_row + i, box_col + j
                    val = board[row][col]
                    if val == 0:
                        continue
                    if val in seen:
                        if generalErrorMessageAdded != True:
                            verifyRegionIn.errorsMessages.append(
                                "Numbers should not be repeated in a region block."
                            )
                            generalErrorMessageAdded = True

                        verifyRegionIn.errorCells.append(
                            wrongCell(
                                x=col,
                                y=row,
                                cellErrorsMessages=["Region block duplicate"],
                            )
                        )
                        prev = seen[val]
                        if not any(
                            e.x == prev[0] and e.y == prev[1]
                            for e in verifyRegionIn.errorCells
                        ):
                            verifyRegionIn.errorCells.append(
                                wrongCell(
                                    x=prev[1],
                                    y=prev[0],
                                    cellErrorsMessages=["Region block duplicate"],
                                )
                            )
                    else:
                        seen[val] = (row, col)
    return verifyRegionIn


# Merge error messages for same cell, it should simplify UI mapping
def merge_error_cells_records(wrongCellsList: List[Dict[str, Any]]) -> List[wrongCell]:
    merged = {}
    for cell in wrongCellsList:
        key = (cell.x, cell.y)

        error = cell.cellErrorsMessages
        if isinstance(error, str):
            error = [error]

        if key not in merged:
            merged[key] = wrongCell(
                x=cell.x, y=cell.y, cellErrorsMessages=list(set(error))
            )
        else:
            merged[key].cellErrorsMessages = sorted(
                list(set(merged[key].cellErrorsMessages + error))
            )

    return list(merged.values())


def verify_empty_cells(verifyEmptyIn: ResponseVerifyGrid):
    oneOfCellsIsEmpty = False
    for row in verifyEmptyIn.grid:
        for val in row:
            if val in (0, None, ""):
                oneOfCellsIsEmpty = True

    if oneOfCellsIsEmpty == True:
        verifyEmptyIn.errorsMessages.append(
            "To finish sudoky all cells should be populated with valuse 1-9."
        )

    return verifyEmptyIn
