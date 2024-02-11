# Prefect Flow
from prefect import task, flow

# Database
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///leads.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

# API Client
import requests
import json
from hashlib import md5

# Environment Variables
from os import environ as env
from dotenv import load_dotenv

load_dotenv()


URL = env.get("SUITECRM_URL")
USERNAME = env.get("SUITECRM_USERNAME")
PASSWORD = env.get("SUITECRM_PASSWORD")


if not all([URL, USERNAME, PASSWORD]):
    raise ValueError("URL, USERNAME and PASSWORD are required")



# Models
class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_work = Column(String)


@flow
def get_leads_data(limit=20):
    # Authentication
    user_auth = {
        "user_name": USERNAME,
        "password": md5(PASSWORD.encode()).hexdigest(),
    }

    # login
    data = {
        "method": "login",
        "input_type": "JSON",
        "response_type": "JSON",
        "rest_data": json.dumps({"user_auth": user_auth, "application_name": "My REST Client", "name_value_list": []}),
    }

    response = requests.post(URL, data=data)

    response.raise_for_status()
    session_id = response.json()["id"]


    # get leads
    data = {
        "method": "get_entry_list",
        "input_type": "JSON",
        "response_type": "JSON",
        "rest_data": json.dumps({
            "session": session_id,
            "module_name": "Leads",
            "query": "",
            "order_by": "",
            "offset": 0,
            "select_fields": ["id", "first_name", "last_name", "phone_work"],
            "link_name_to_fields_array": [],
            "max_results": limit,
            "deleted": 0,
        }),
    }

    response = requests.post(URL, data=data)
    response.raise_for_status()

    return response.json()



@flow
def transform_leads_data(data):
    return [
        {
            "id": lead["id"],
            "first_name": lead["name_value_list"]["first_name"]["value"],
            "last_name": lead["name_value_list"]["last_name"]["value"],
            "phone_work": lead["name_value_list"]["phone_work"]["value"],
        }
        for lead in data["entry_list"]
    ]



@flow
def save_leads_data(data):
    Base.metadata.create_all(engine)
    if session.query(Lead).count() > 0:
        session.query(Lead).delete()
    for lead in data:
        session.add(Lead(**lead))
    session.commit()


@flow()
def main():
    leads_data = get_leads_data()
    transformed_leads_data = transform_leads_data(leads_data)
    save_leads_data(transformed_leads_data)


if __name__ == "__main__":
    main.serve(
        name="SuiteCRM Leads",
        cron="0 0 * * *",
    )