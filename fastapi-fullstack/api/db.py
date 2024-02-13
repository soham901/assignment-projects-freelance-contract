import requests
import json
from hashlib import md5
from os import environ as env
from dotenv import load_dotenv

import pymongo


load_dotenv()

URL = env.get("SUITECRM_URL")
USERNAME = env.get("SUITECRM_USERNAME")
PASSWORD = env.get("SUITECRM_PASSWORD")

DB_URL = env.get("MONGO_URL")
DB_NAME = env.get("MONGO_DB_NAME")
DB_COLLECTION = env.get("MONGO_DB_COLLECTION")


if not all([URL, USERNAME, PASSWORD, DB_URL, DB_NAME, DB_COLLECTION]):
    raise ValueError("URL, USERNAME and PASSWORD and DB_URL, DB_NAME, DB_COLLECTION must be set in .env file")



client = pymongo.MongoClient(DB_URL)
db = client[DB_NAME]
collection = db[DB_COLLECTION]

print("Connected to DB :::::::::::::::::::::::::::::::::::::::::::::::::::::::::")


def get_leads_from_api(limit=200):
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



def get_leads_from_db():
    data = list(collection.find({}))
    # convert object id to string
    data = [{**lead, "_id": str(lead["_id"])} for lead in data]
    return data


def save_leads_to_db(leads):
    collection.insert_many(leads)


def get_leads():
    leads = get_leads_from_db()
    if not leads:
        leads = transform_leads_data(get_leads_from_api())
        save_leads_to_db(leads)
    return leads
