from board import make_boardCell


def test_default_BoardCell():
    defaultBoardCell = make_boardCell(0, 992)
    assert defaultBoardCell.x is 0
    assert defaultBoardCell.y is 992
    assert defaultBoardCell.changeable is True
    assert defaultBoardCell.value is None


def test_BoardCell_for_non_editable_cell():
    boardCellForNonEditable = make_boardCell(1, 2, False, 5)
    assert boardCellForNonEditable.x == 1
    assert boardCellForNonEditable.y == 2
    assert boardCellForNonEditable.changeable == False
    assert boardCellForNonEditable.value == 5


# TODO add boardCellForNonEditable.value from 1 to 9
