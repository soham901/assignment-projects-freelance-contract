from fastapi import FastAPI

from manage_data import get_leads

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Health": "OK"}




@app.get("/leads")
def read_leads():
    data = get_leads()
    return {"data": data}