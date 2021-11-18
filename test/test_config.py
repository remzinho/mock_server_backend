from helpers.utils import *
import pytest

def test_getConfig():
    """
    Tests simple dashboard calls.
    """
    token = get_auth_token("usr1", "pass1")
    r = get_config(token=token)

    assert r.status_code == 200
    check_property_in_response(r, "state", "config")
    check_property_in_response(r, "token", token)
    check_property_in_response(r, "uid", 1)
    check_property_in_response(r, "user", "usr1")
    check_property_in_response(r, "password", "pass1")
    check_property_in_response(r, "allowed_items", ["item1", "item2", "item4"])

@pytest.mark.last
def test_updateConfig():
    token = get_auth_token("usr1", "pass1")
    body = {
        "username": "usr3",
        "password":  "asd",
        "allowed_items": ["item1", "item2"]
    }
    r = put_config(body, token=token)
    assert r.status_code == 200
    # validate state/view change
    check_property_in_response(r, "state", "login")

    # validate changes to the user
    token = get_auth_token("usr3", "asd")
    r = get_config(token=token)
    assert r.status_code == 200
    check_property_in_response(r, "token", token)
    check_property_in_response(r, "uid", 1)
    check_property_in_response(r, "user", "usr3")
    check_property_in_response(r, "password", "asd")
    check_property_in_response(r, "allowed_items", ["item1", "item2"])

    # test config change request
    token = get_auth_token("usr3", "asd")
    body = {
        "username": "usr1",
        "password":  "pass1",
    }
    r = put_config(body, token=token)
    assert r.status_code == 200
    check_property_in_response(r, "state", "login")
    
    # check for partial config changes
    token = get_auth_token("usr1", "pass1")
    r = get_config(token=token)
    assert r.status_code == 200
    check_property_in_response(r, "user", "usr1")
    check_property_in_response(r, "password", "pass1")
    check_property_in_response(r, "allowed_items", ["item1", "item2"])

    # "cleanup"
    token = get_auth_token("usr1", "pass1")
    body = {
        "allowed_items": ["item1", "item2", "item4"]
    }
    r = put_config(body, token=token)
    assert r.status_code == 200
