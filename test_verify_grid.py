from board_mocks import mock1, mock2, mock1_resolved_as_array, mock1_as_array
from verify_grid import verify_grid, wrongCell
import copy


def test_verify_grid_response_happy_path_resolved_mock1():
    verifyGrifResult = verify_grid("mock1", mock1_resolved_as_array)
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that this value returned in response
    assert verifyGrifResult.grid == mock1_resolved_as_array
    # and no errors
    assert verifyGrifResult.errorCells == []
    assert verifyGrifResult.errorsMessages == []


def test_verify_grid_response_happy_path_one_change():
    oneChangeArray = copy.deepcopy(mock1_as_array)
    # Here we simulate change 0 to good value 5 in x:3,y:5
    (oneChangeArray[5])[3] = 5

    verifyGrifResult = verify_grid("mock1", oneChangeArray)
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that this value returned in response
    assert (verifyGrifResult.grid[5])[3] == 5
    assert verifyGrifResult.grid == oneChangeArray
    assert verifyGrifResult.errorCells == []
    assert verifyGrifResult.errorsMessages == [
        "To finish sudoky all cells should be populated with valuse 1-9."
    ]


def test_verify_grid_response_happy_path_not_finished_game_five_changes():
    fiveChangesArray = copy.deepcopy(mock1_as_array)
    # Here we simulate change 0 to good value 5 in x:3,y:5
    (fiveChangesArray[0])[8] = 4
    (fiveChangesArray[1])[7] = 3
    (fiveChangesArray[2])[3] = 2
    (fiveChangesArray[4])[4] = 5
    (fiveChangesArray[7])[1] = 2

    verifyGrifResult = verify_grid("mock1", fiveChangesArray)

    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that these values are returned in response
    assert verifyGrifResult.grid == fiveChangesArray
    assert verifyGrifResult.errorCells == []
    assert verifyGrifResult.errorsMessages == [
        "To finish sudoky all cells should be populated with valuse 1-9."
    ]


def test_verify_grid_cheating_error():
    cheatingChangesArray = copy.deepcopy(mock1_as_array)
    # Here we simulate change noneditable 5 to bad value 0 in x:0,y:0
    # and change noneditable 3 to good bad 1 in x:1,y:0
    # and change 0 to good value 3 in x:7,y:1
    # and change 8 to bad value 2 in x:3,y:4
    # and change 0 to good value 5 in x:2,y:5
    (cheatingChangesArray[0])[0] = 0
    (cheatingChangesArray[0])[1] = 0
    (cheatingChangesArray[1])[7] = 3
    (cheatingChangesArray[4])[3] = 2
    (cheatingChangesArray[5])[2] = 5

    verifyGrifResult = verify_grid("mock1", cheatingChangesArray)
    assert verifyGrifResult.gridId == "mock1"
    # And expecting that non editable values are fixed and returned in response
    revertedFixedValuesExpected = cheatingChangesArray
    (revertedFixedValuesExpected[0])[0] = 5
    (revertedFixedValuesExpected[0])[1] = 3
    (revertedFixedValuesExpected[4])[3] = 8
    assert verifyGrifResult.grid == revertedFixedValuesExpected
    assert len(verifyGrifResult.errorCells) == 3
    assert verifyGrifResult.errorCells == [
        wrongCell(x=0, y=0, cellErrorsMessages=["Cheating"]),
        wrongCell(x=0, y=1, cellErrorsMessages=["Cheating"]),
        wrongCell(x=4, y=3, cellErrorsMessages=["Cheating"]),
    ]
    assert (
        verifyGrifResult.errorsMessages[0]
        == "No cheating! You cannot change the starting grid values."
    )


def test_verify_grid_response_vertical_duplicate_error():
    verticalDuplicatesChangesArray = copy.deepcopy(mock1_as_array)
    # Here we simulate change 0 to bad value 7 in x:7,y:1
    # and change 0 to good value 5 in x:4,y:4
    (verticalDuplicatesChangesArray[1])[7] = 7
    (verticalDuplicatesChangesArray[4])[4] = 5

    verifyGrifResult = verify_grid("mock1", verticalDuplicatesChangesArray)

    print(mock1_as_array)
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[1])[7] == 7
    assert verifyGrifResult.grid == verticalDuplicatesChangesArray
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=7, y=8, cellErrorsMessages=["Vertical row duplicate"]
    )
    assert verifyGrifResult.errorCells[1] == wrongCell(
        x=7, y=1, cellErrorsMessages=["Vertical row duplicate"]
    )
    assert (
        verifyGrifResult.errorsMessages[0]
        == "Numbers should not be repeated in a vertical row."
    )


def test_verify_grid_response_horisontal_duplicate_error():
    horisontlDuplicatesChangesArray = copy.deepcopy(mock1_as_array)
    # Here we simulate change 0 to bad value 9 in x:7,y:1
    # and change 0 to good value 5 in x:4,y:4
    (horisontlDuplicatesChangesArray[1])[7] = 9
    (horisontlDuplicatesChangesArray[4])[4] = 5

    verifyGrifResult = verify_grid("mock1", horisontlDuplicatesChangesArray)
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[1])[7] == 9
    assert verifyGrifResult.grid == horisontlDuplicatesChangesArray
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=7, y=1, cellErrorsMessages=["Horisontal row duplicate"]
    )
    assert verifyGrifResult.errorCells[1] == wrongCell(
        x=4, y=1, cellErrorsMessages=["Horisontal row duplicate"]
    )
    assert (
        verifyGrifResult.errorsMessages[0]
        == "Numbers should not be repeated in a horizontal row."
    )


def test_verify_grid_response_region_duplicate_error():
    regionDuplicatesChangesArray = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 1, 0, 6],
        [0, 6, 0, 0, 4, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 4, 0, 7, 9],
    ]

    verifyGrifResult = verify_grid("mock1", regionDuplicatesChangesArray)
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that all these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[5])[6] == 1
    assert (verifyGrifResult.grid[4])[8] == 1
    assert (verifyGrifResult.grid[8])[5] == 4
    assert (verifyGrifResult.grid[7])[3] == 4
    assert (verifyGrifResult.grid[6])[4] == 4
    assert verifyGrifResult.grid == regionDuplicatesChangesArray
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 5
    assert verifyGrifResult.errorCells == [
        wrongCell(x=6, y=5, cellErrorsMessages=["Region block duplicate"]),
        wrongCell(x=8, y=4, cellErrorsMessages=["Region block duplicate"]),
        wrongCell(x=3, y=7, cellErrorsMessages=["Region block duplicate"]),
        wrongCell(x=4, y=6, cellErrorsMessages=["Region block duplicate"]),
        wrongCell(x=5, y=8, cellErrorsMessages=["Region block duplicate"]),
    ]

    assert verifyGrifResult.errorsMessages == [
        "Numbers should not be repeated in a region block.",
        "To finish sudoky all cells should be populated with valuse 1-9.",
    ]


def test_verify_grid_response_empty_cells_error():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate that few cells still not populated
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 0, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 0, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid == [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 0, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 0, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    # Empty cells is not an cell error as it's normal game process
    assert len(verifyGrifResult.errorCells) == 0
    # But we want to propagate this as a message to UI
    assert verifyGrifResult.errorsMessages == [
        "To finish sudoky all cells should be populated with valuse 1-9."
    ]


def test_verify_grid_response_for_vertical_and_horisontal_duplicates_errors():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 0 to bad value 8 in x:2,y:6
            # So expected receive duplication errors with 2:2 and 7:6
            # and change 0 to good value 5 in x:4,y:4
            # and change 8 to bad value 6 in x:7,y:6 which should be reverted without duplication errors
            # and change 0 to bad value 6 in x:8,y:2 which conflicted with all types vertical, horisontal, region
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 6],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 8, 0, 0, 0, 2, 6, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[6])[2] == 8
    assert (verifyGrifResult.grid[4])[4] == 5
    # And owervriting reverted
    assert (verifyGrifResult.grid[6])[7] == 8
    assert verifyGrifResult.grid == [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 6],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 8, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 8
    assert verifyGrifResult.errorCells == [
        wrongCell(x=6, y=7, cellErrorsMessages=["Cheating"]),
        wrongCell(
            x=2,
            y=6,
            cellErrorsMessages=["Horisontal row duplicate", "Vertical row duplicate"],
        ),
        wrongCell(x=2, y=2, cellErrorsMessages=["Vertical row duplicate"]),
        wrongCell(x=8, y=5, cellErrorsMessages=["Vertical row duplicate"]),
        wrongCell(
            x=8,
            y=1,
            cellErrorsMessages=[
                "Horisontal row duplicate",
                "Region block duplicate",
                "Vertical row duplicate",
            ],
        ),
        wrongCell(x=0, y=1, cellErrorsMessages=["Horisontal row duplicate"]),
        wrongCell(x=7, y=6, cellErrorsMessages=["Horisontal row duplicate"]),
        wrongCell(x=7, y=2, cellErrorsMessages=["Region block duplicate"]),
    ]
    assert verifyGrifResult.errorsMessages == [
        "No cheating! You cannot change the starting grid values.",
        "Numbers should not be repeated in a vertical row.",
        "Numbers should not be repeated in a horizontal row.",
        "Numbers should not be repeated in a region block.",
        "To finish sudoky all cells should be populated with valuse 1-9.",
    ]
