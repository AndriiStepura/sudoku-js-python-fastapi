from verify_grid import verify_grid, wrongCell


def test_verify_grid_response_happy_path_one_change():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that this value returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert verifyGrifResult.grid == [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    assert verifyGrifResult.errorCells == []
    assert verifyGrifResult.errorsMessages == []


def test_verify_grid_cheating_error():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 5 to bad value 0 in x:0,y:0
            # and change 0 to good value 3 in x:7,y:1
            # and change 8 to bad value 2 in x:3,y:4
            # and change 0 to good value 5 in x:2,y:5
            [0, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 3, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 2, 0, 3, 0, 0, 1],
            [7, 0, 5, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    # And expecting that non editable values are fixed and returned in response
    assert verifyGrifResult.grid == [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 3, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 5, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=0, y=0, cellErrorMessage="Cheating"
    )
    assert verifyGrifResult.errorCells[1] == wrongCell(
        x=4, y=3, cellErrorMessage="Cheating"
    )
    assert (
        verifyGrifResult.errorsMessages[0]
        == "No cheating! You cannot change the starting grid values."
    )


def test_verify_grid_response_vertical_duplicate_error():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 0 to bad value 7 in x:7,y:1
            # and change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 7, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[1])[7] == 7
    assert verifyGrifResult.grid == [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 7, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=7, y=8, cellErrorMessage="Vertical row duplicate"
    )
    assert verifyGrifResult.errorCells[1] == wrongCell(
        x=7, y=1, cellErrorMessage="Vertical row duplicate"
    )
    assert (
        verifyGrifResult.errorsMessages[0]
        == "Numbers should not be repeated in a vertical row."
    )


def test_verify_grid_response_horisontal_duplicate_error():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 0 to bad value 9 in x:7,y:1
            # and change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 9, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[1])[7] == 9
    assert verifyGrifResult.grid == [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 9, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=7, y=1, cellErrorMessage="Horisontal row duplicate"
    )
    assert verifyGrifResult.errorCells[1] == wrongCell(
        x=4, y=1, cellErrorMessage="Horisontal row duplicate"
    )
    assert (
        verifyGrifResult.errorsMessages[0]
        == "Numbers should not be repeated in a horizontal row."
    )


def test_verify_grid_response_area_duplicate_error():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 0 to bad value 6 in x:1,y:7
            # and change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 6, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ],
    )
    assert verifyGrifResult.gridId == "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[7])[1] == 6
    assert verifyGrifResult.grid == [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 9, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 6, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=1, y=6, cellErrorMessage="Region block duplicate"
    )
    assert verifyGrifResult.errorCells[0] == wrongCell(
        x=1, y=7, cellErrorMessage="Region block duplicate"
    )
    assert (
        verifyGrifResult.errorsMessages
        == "Numbers should not be repeated in region block."
    )


def test_verify_grid_response_for_vertical_and_horisontal_duplicates_errors():
    verifyGrifResult = verify_grid(
        "mock1",
        [
            # Here we simulate change 0 to bad value 8 in x:2,y:6
            # So expected receive dublication errors with 2:2 and 7:6
            # and change 0 to good value 5 in x:4,y:4
            # and change 8 to bad value 6 in x:7,y:6 which should be reverted without dublication errors
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
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
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 5, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 8, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 5
    assert verifyGrifResult.errorCells == [
        wrongCell(x=6, y=7, cellErrorMessage="Cheating"),
        wrongCell(x=2, y=6, cellErrorMessage="Vertical row duplicate"),
        wrongCell(x=2, y=2, cellErrorMessage="Vertical row duplicate"),
        wrongCell(x=7, y=6, cellErrorMessage="Horisontal row duplicate"),
        wrongCell(x=2, y=6, cellErrorMessage="Horisontal row duplicate")
    ]
    assert (
        verifyGrifResult.errorsMessages == [
            "No cheating! You cannot change the starting grid values.",
            "Numbers should not be repeated in a vertical row.",
            "Numbers should not be repeated in a horizontal row."
        ]        
    )
