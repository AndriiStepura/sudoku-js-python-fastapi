from verify_grid import verify_grid, wrongCell


def test_verify_grid_response_happy_path_one_change():
    verifyGrifResult = verify_grid("mock1",[
        # Here we simulate change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    )    
    assert verifyGrifResult.gridId is "mock1"
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
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]    
    assert verifyGrifResult.errorCells == []
    assert verifyGrifResult.errorsMessage == None


def test_verify_grid_cheating_error():
    verifyGrifResult = verify_grid("mock1",[
        # Here we simulate change 5 to bad value 0 in x:0,y:0
        # and change 0 to good value 3 in x:7,y:1
        # and change 8 to bad value 2 in x:3,y:4
        # and change 0 to good value 3 in x:2,y:5
            [0, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 3, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 2, 0, 3, 0, 0, 1],
            [7, 0, 5, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    )
    assert verifyGrifResult.gridId is "mock1"
    # And expecting that these values are returned in response
    assert verifyGrifResult.grid == [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 3, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 5, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]    
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(x=0, y=0, cellErrorMessage="Cheating")
    assert verifyGrifResult.errorCells[1] == wrongCell(x=3, y=4, cellErrorMessage="Cheating")
    assert verifyGrifResult.errorsMessage == "No cheating! You cannot change the starting grid values."


def test_verify_grid_response_vertical_duplicate_error():
    verifyGrifResult = verify_grid("mock1",[
        # Here we simulate change 0 to bad value 8 in x:5,y:2
        # and change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 8, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    )    
    assert verifyGrifResult.gridId is "mock1"
    assert verifyGrifResult.grid != []
    # And expecting that both these values are returned in response
    assert (verifyGrifResult.grid[4])[4] == 5
    assert (verifyGrifResult.grid[2])[5] == 8
    assert verifyGrifResult.grid == [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 8, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(x=2, y=2, cellErrorMessage="Vertical row duplicate")
    assert verifyGrifResult.errorCells[0] == wrongCell(x=5, y=2, cellErrorMessage="Vertical row duplicate")
    assert verifyGrifResult.errorsMessage == "Numbers should not be repeated in a vertical row."


def test_verify_grid_response_horisontal_duplicate_error():
    verifyGrifResult = verify_grid("mock1",[
        # Here we simulate change 0 to bad value 9 in x:7,y:1
        # and change 0 to good value 5 in x:4,y:4
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 9, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 5, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 7, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    )    
    assert verifyGrifResult.gridId is "mock1"
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
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(x=4, y=0, cellErrorMessage="Horisontal row duplicate")
    assert verifyGrifResult.errorCells[0] == wrongCell(x=5, y=2, cellErrorMessage="Horisontal row duplicate")
    assert verifyGrifResult.errorsMessage == "Numbers should not be repeated in a horizontal row."


def test_verify_grid_response_area_duplicate_error():
    verifyGrifResult = verify_grid("mock1",[
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
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    )    
    assert verifyGrifResult.gridId is "mock1"
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
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    # So response should back with both wrong cells data for UI
    assert len(verifyGrifResult.errorCells) == 2
    assert verifyGrifResult.errorCells[0] == wrongCell(x=1, y=6, cellErrorMessage="Region block duplicate")
    assert verifyGrifResult.errorCells[0] == wrongCell(x=1, y=7, cellErrorMessage="Region block duplicate")
    assert verifyGrifResult.errorsMessage == "Numbers should not be repeated in region block."
