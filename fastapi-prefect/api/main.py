from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import db
import utils


app = FastAPI()


@app.get("/")
def read_root():
    count = len(db.get_leads())
    return {"Health": "OK", "lead_count": count}



@app.get("/sync-leads")
def sync_leads():
    try:
        data = utils.get_leads_from_api()
        print(f"Syncing {len(data)} leads")

        for lead in data:
            db.create_lead(lead)

        return {"message": "Sync successful"}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))



@app.get("/leads")
def read_leads():
    return db.get_leads()



@app.get("/leads/{id}")
def read_lead(id: str):
    return db.get_lead(id)



@app.post("/leads")
def create_lead(data: dict):
    # it wil update the lead if it already exists
    return db.create_lead(data)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
