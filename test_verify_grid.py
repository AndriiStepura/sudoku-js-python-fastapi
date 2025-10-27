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
    assert verifyGrifResult.errorsMessage is None


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

    
