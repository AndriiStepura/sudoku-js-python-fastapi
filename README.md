# sudoku-js-python-fastapi

POC with python FastAPI based on Sudoku puzzle logic
Git repo - https://github.com/AndriiStepura/sudoku-js-python-fastapi

# How to run

## Back-end
For back-end API env to run preconditions are:
1. Python - v3+ https://www.python.org/downloads/
2. pip - https://packaging.python.org/en/latest/tutorials/installing-packages/
3. fastapi and uvicorn packages, can be installed with:
```
pip install fastapi
pip install uvicorn
```

To run back-end python with fast API in root folder path execute in terminal:
`uvicorn main:app --reload`

### Endpoints notes

Documentation - http://127.0.0.1:8000/docs

Health check endpoint GET /
`curl --location 'http://127.0.0.1:8000/'`

Get new game board GET /newgrid
`curl --location 'http://127.0.0.1:8000/newgrid'`

Get new game board POST /verifygrid  
`curl --location 'http://127.0.0.1:8000/verifygrid'`  
PARAMS TBD

#### Unit tests

We use pytest for unit tests to configure your VSC IDE run:  
`Python: Configure Tests`

To run all unit tests:  
`python -m pytest -vv`

To debug app locally in VSC IDE follow guide  
https://fastapi.tiangolo.com/tutorial/debugging/#run-your-code-with-your-debugger
or navigate to Run and Debug (Ctrl+Shift+D and F5 to start)

#### Formatting

https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter


## Front-end
Located in /front-end/ path, based on [Pico CSS Pure HTML](https://picocss.com/examples)  





# Few general important notes about implementation

1. If you have requirements that sudoku will be always 9\*9 and with single possible solution it make more sense just to store starting grid and proper solution and just compare user attempt with proper one to highlight diviations.
   But in my case requirements unclear, also some future versions may allow bigger sudoku with 16×16 area or easier level which may allow multiply solutions, that's why I implemented validation (vertical, horisontal and region) based on user imput

2. Gameboard im my implementation is represented by array of arrays and two notes to keep in mind for proper usage as it's abstract and may be an umbigues
   First of all when you call this board, for example RequestVerifyGrid.grid you need to use reversed y after x so use (RequestVerifyGrid.grid[y])[x]
   And numeration from top right corner, so x:y coordinates mapped in array:
   [
   [0:0 , 0:1, 0:2],
   [1:0 , 1:1, 1:2],
   [2:0 , 2:1, 2:2]
   ]
