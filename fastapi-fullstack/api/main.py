from fastapi import FastAPI

from db import get_leads

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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000)
