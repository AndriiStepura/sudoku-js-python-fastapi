import json
from json import JSONEncoder
from board_mocks import convert_board, make_boardCell


# subclass JSONEncoder to make class BoardCell serializable
class BoardEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


# Test mock converter helper
def test_default_BoardCell():
    expectedMockForJSON = [
        {
            "x": 0,
            "y": 0,
            "changeable": True,
            "value": None,
        },
        {
            "x": 0,
            "y": 1,
            "changeable": False,
            "value": 5,
        },
        {
            "x": 1,
            "y": 0,
            "changeable": False,
            "value": 9,
        },
        {
            "x": 1,
            "y": 1,
            "changeable": True,
            "value": None,
        },
    ]

    mock_as_ints = [[0, 5], [9, 0]]
    result = convert_board(mock_as_ints)

    # This asserts equality *by values* (deep comparison)
    # "Converting a Python object to a JSON string using json.dumps():"
    # by https://www.zyte.com/blog/json-parsing-with-python/
    assert BoardEncoder().encode(result) == json.dumps(expectedMockForJSON)
