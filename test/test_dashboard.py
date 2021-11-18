from flask.json import jsonify
from helpers.utils import *


def test_dashboardSanity():
    """
    Tests simple dashboard calls.
    """
    r = get_dashboard()
    assert r.status_code == 200
    check_property_in_response(r, "state", "dashboard")

def test_dashboardFromDifferentUser():
    r = get_dashboard("usr2", "pass2")
    assert r.status_code == 200
    check_property_in_response(r, "state", "dashboard") 
    check_property_in_response(r, "logged_user", "usr2") 

def test_getAllItems():
    r = get_items()
    print(r.text)
    assert r.status_code == 200

def test_pagination():
    page_size = 5
    r = get_items(extraParameters="?page=1&pageSize={}".format(page_size))
    assert r.status_code == 200
    item_list = json.loads(r.text)
    assert len(item_list) == page_size

def test_ordering():
    r = get_items(extraParameters="?page=1&pageSize=50&sortBy=date&sortOrder=desc")
    assert True

def test_sanitization():
    # little Bobby tables
    # try an SQL injection
    r = get_items(extraParameters="?page=1&pageSize=50&sortBy=date&sortOrder=asc&filterField=state&filterValue=running');DROP TABLE items; --")
    assert r.status_code == 500
    # see if the server is up and running afterwards
    r = get_items(extraParameters="?page=1&pageSize=5")
    assert r.status_code == 200
    item_list = json.loads(r.text)
    assert len(item_list) == 5
