import json

from pymongo import MongoClient



def extract_data():
    data = json.load(open('data.json'))

    new_data = []

    for i, d in enumerate(data):
        attrubutes = d.get("attributes")
        phone_work = attrubutes.get("phone_work")
        first_name = attrubutes.get("first_name")
        last_name = attrubutes.get("last_name")

        new_data.append({
            "id": attrubutes.get("id"),
            "first_name": first_name,
            "last_name": last_name,
            "phone_work": phone_work
        })

        print(f"{i+1}. {first_name} {last_name} - {phone_work}")

        json.dump(new_data, open('final_data.json', 'w'), indent=4)



def save_data_to_mongodb(url: str, data: list):

    client = MongoClient(url)
    db = client['demo-db']
    collection = db['leads']

    collection.insert_many(data)

    print("Data saved to MongoDB")



if __name__ == "__main__":
    try:
        json.load(open('final_data.json'))
    except FileNotFoundError:
        extract_data()
    finally:
        data = json.load(open('final_data.json'))
        save_data_to_mongodb('mongodb://localhost:27017/', data)
