# Prefect Flow
from prefect import flow, task

# API Client
import requests
import json


BASE_URL = "http://127.0.0.1:8000"


@flow(name="Sync Leads")
def sync_leads():
    try:
        response = requests.get(f"{BASE_URL}/sync-leads")

        if response.status_code == 200:
            print("Leads Synced")
            return response.json()
        
        print(f"Error: {response.status_code}")
        return {
            "error": "Error syncing leads"
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "error": "Error syncing leads"
        }


if __name__ == "__main__":
    sync_leads.serve(
        name="SuiteCRM Leads",
        cron="0 0 * * *",
    )
