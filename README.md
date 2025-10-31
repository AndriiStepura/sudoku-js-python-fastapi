# sudoku-js-python-fastapi

POC with python FastAPI based on Sudoku puzzle logic
Git repo - https://github.com/AndriiStepura/sudoku-js-python-fastapi

# How to run

## Back-end (cd backend)

For back-end API env to run preconditions are:

1. Python - v3+ https://www.python.org/downloads/
2. pip - https://packaging.python.org/en/latest/tutorials/installing-packages/
3. fastapi and uvicorn packages, can be installed with:

```
pip install fastapi
pip install uvicorn
```

To run backend from local code in `cd backend` folder path execute in terminal:
`uvicorn main:app --reload --host 127.0.0.1 --port 8000`

And switch front-end config to proper back-end in first lines `/frontend/static/sudoku.js`
For local run and debug use `http://127.0.0.1:8000`
For dokerized default is `http://localhost:8000`

### Endpoints notes

Root http://127.0.0.1:8000/ return front-end from /frontend/index.html

Documentation - http://127.0.0.1:8000/docs

API health check endpoint GET /v1/  
`curl --location 'http://127.0.0.1:8000/v1/'`

Get new game board GET /newgrid  
`curl --location 'http://127.0.0.1:8000/v1/newgrid'`

To verify puzzle send player input to POST /verifygrid  
```
curl --location 'http://127.0.0.1:8000/v1/verifygrid/' \
--header 'Content-Type: application/json' \
--data '{
  "gridId": "mock1",
  "grid": [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 0, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 0, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
]
}'
```

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

Located in /frontend/ path, based on [Pico CSS Pure HTML](https://picocss.com/examples)

## Docker
Image in Docker hub - https://hub.docker.com/r/andriistepura30602/sudokujspythonfastapi 
you can pill and run:
```
docker pull andriistepura30602/sudokujspythonfastapi
docker run -d --name mysudokucontainer -p 8000:8000 docker.io/andriistepura30602/sudokujspythonfastapi:latest
```
and open in browser http://localhost:8000/


[FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/)  

0. Generate dependencies (when bump-up) 
   `pip3 freeze > requirements.txt`

1.  To build the Docker Image:
    `docker build -t sudokujspythonfastapi:v1.1 .`

2.  Start the Docker Container:
    `docker run -d --name mysudokucontainer -p 8000:8000 docker.io/andriistepura30602/sudokujspythonfastapi:latest`

3.  To open in browser UI (frontend) from container which connected to backend in the same container:
    pos


<hr>


# Few general important notes about implementation

1. If you have requirements that sudoku will be always 9\*9 and with single possible solution it make more sense just to store starting grid and proper solution and just compare user attempt with proper one to highlight diviations.
   But in my case requirements unclear, also some future versions may allow bigger sudoku with 16×16 area or easier level which may allow multiply solutions, that's why I implemented validation (vertical, horisontal and region) based on user input

2. Gameboard im my implementation is represented by array of arrays and two notes to keep in mind for proper usage as it's abstract and may be an umbigues
   as first of all when you call this board, for example RequestVerifyGrid.grid you need to use reversed y after x so use (RequestVerifyGrid.grid[y])[x]
   And numeration from top right corner, so x:y coordinates mapped in array:
```   
   [
      [0:0 , 0:1, 0:2, ... , 0:8],
      [1:0 , 1:1, 1:2, ... , 1:8],
      [2:0 , 2:1, 2:2, ... , 2:8],
      ...........................
      [8:0 , 2:1, 2:2, ... , 8:8],
   ]
```   