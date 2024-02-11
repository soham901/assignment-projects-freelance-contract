from prefect import task, flow

@flow
def login(user_auth):
    return "1234"


@flow
def get_data(limit=20):
    user_auth = {
        "user_name": "USERNAME",
        "password": "PASSWORD",
    }
    session_id = login(user_auth)
    return [{"id": 1, "first_name": "John", "last_name": "Doe", "phone_work": "1234567890"}] * limit



print(get_data(4))