from flask.json import jsonify
import requests, json
import globals, pytest

@pytest.fixture(autouse=True)
def populate_globals():
    globals.urls = {
        "host": "http://127.0.0.1:5000",
        "login": "http://127.0.0.1:5000/login",
        "dashboard": "http://127.0.0.1:5000/dashboard",
        "items": "http://127.0.0.1:5000/items",
        "config": "http://127.0.0.1:5000/config"
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

def get_dashboard(user="usr1", password="pass1", token=""):
    if token != "":
        headers = {'Authorization': token}
    else:
        headers = {'Authorization': get_auth_token(user, password)}
    return requests.get(globals.urls["dashboard"], headers=headers)

def get_items(extraParameters = "", user="usr1", password="pass1", token=''):
    headers = {'Authorization': get_auth_token(user, password)}
    return requests.get(globals.urls["items"] + extraParameters, headers=headers)

def get_config(user="usr1", password="pass1", token=""):
    if token != "":
        headers = {'Authorization': token}
    else:
        headers = {'Authorization': get_auth_token(user, password)}
    return requests.get(globals.urls["config"], headers=headers)

def put_config(body, user="usr1", password="pass1", token=""):
    if token != "":
        headers = {'Authorization': token, "Content-Type": "application/json"}
    else:
        headers = {'Authorization': get_auth_token(user, password)}
    print("-----")
    print(body)
    return requests.put(globals.urls["config"], data=json.dumps(body), headers=headers)