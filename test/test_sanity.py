import requests, json

host = "http://127.0.0.1:5000"
login_page = host + "/login"


def test_serverUp():
    """
    Tests if the server it up and running
    """
    r = requests.get(login_page)
    assert r.status_code == 200

    r = requests.get(host)
    assert r.status_code == 404

def test_simpleLogin():
    req_data = {
        "username": "usr1",
        "password": "pass1"
    }
    headers = {'Content-type': 'application/json'}
    r = requests.post(login_page, data=json.dumps(req_data), headers=headers)
    print(r.text)
    assert r.status_code == 200
