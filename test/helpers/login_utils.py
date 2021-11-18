import requests, json
import globals, pytest

@pytest.fixture(autouse=True)
def populate_globals():
    globals.urls = {
        "host": "http://127.0.0.1:5000",
        "login": "http://127.0.0.1:5000/login"
    }

def login_with(user, password):
    req_data = {
        "username": user,
        "password": password
    }
    headers = {'Content-type': 'application/json'}
    return requests.post(globals.urls["login"], data=json.dumps(req_data), headers=headers)

def check_property_in_response(request_obj, key, expected_val):
    response_dict = json.loads(request_obj.text)
    assert response_dict[key] == expected_val

def get_property_in_response(request_obj, key):
    response_dict = json.loads(request_obj.text)
    return response_dict[key]

def get_auth_token(user, password):
    return get_property_in_response(login_with(user, password),"session_token")
