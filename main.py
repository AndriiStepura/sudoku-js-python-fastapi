from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "I'm sudoku back-end with python FastAPI"}