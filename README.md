# sudoku-js-python-fastapi
POC with python FastAPI based on Sudoku puzzle logic
Git repo - https://github.com/AndriiStepura/sudoku-js-python-fastapi


# How to run
Back-end env run preconditions are:
1. Python - v3+ https://www.python.org/downloads/
2. pip - https://packaging.python.org/en/latest/tutorials/installing-packages/
3. fastapi and uvicorn packages:
```
pip install fastapi
pip install uvicorn
```

To run back-end python with fast API in root folder path execute in terminal:
```uvicorn main:app --reload```


# Endpoints notes
Health check endpoint GET /
```curl --location 'http://127.0.0.1:8000/'```  


Get new game board GET /newgrid
```curl --location 'http://127.0.0.1:8000/newgrid'```  


Get new game board POST /verifygrid  
```curl --location 'http://127.0.0.1:8000/verifygrid'```  
PARAMS TBD


# Unit tests
We use pytest for unit tests to configure your VSC IDE run:  
```Python: Configure Tests```

To run all unit tests:  
```python -m pytest -vv```