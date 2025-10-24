from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "I'm sudoku back-end with python FastAPI"}

@app.get("/newgrid")
def root():
    return {
            "grid": [
                     {"a1":"TBD grid cell #1"},
                     {"a2":"TBD grid cell #2"},
                     {"a3":"TBD grid cell #3"}
                    ],
            "error": None
        }