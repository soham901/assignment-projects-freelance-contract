import json
from fastapi import FastAPI


data = json.load(open("final_data.json"))

app = FastAPI()


@app.get("/")
def read_root():
    return {"Health": "OK"}
