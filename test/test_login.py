from helpers.utils import *


def test_simpleLogin():
    """
    Tests simple login.
    """
    r = login_with("usr1", "pass1")
    check_property_in_response(r, "message", "Login successful!")
    check_property_in_response(r, "state", "dashboard")
    assert r.status_code == 200

    # incorrect credentials
    r = login_with("usr1", "pass2")
    check_property_in_response(r, "message", "Wrong username/password!")
    assert r.status_code == 401

    # non existing credentials
    r = login_with("usr3", "pass3")
    check_property_in_response(r, "message", "Wrong username/password!")
    assert r.status_code == 401

def test_differentTokenEachTime():
    # tokens shoould be different for each login
    r = login_with("usr1", "pass1")
    prev_token = get_property_in_response(r, "session_token")
    r = login_with("usr1", "pass1")
    new_token = get_property_in_response(r, "session_token")
    assert prev_token != new_token

