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


def test_dashboardUnauthorizedSession():
    token1 = get_auth_token("usr1", "pass1")
    token2 = get_auth_token("usr1", "pass1")
    r = get_dashboard(token=token1)
    assert r.status_code == 401


def test_getAllItems():
    r = get_items(extraParameters="?page=1&pageSize=999")
    assert r.status_code == 200
    item_list = json.loads(r.text)
    assert len(item_list) == 6


def test_pagination():
    page_size = 5
    r = get_items(extraParameters="?page=1&pageSize={}".format(page_size))
    assert r.status_code == 200
    item_list = json.loads(r.text)
    assert len(item_list) == page_size


def test_ordering():
    r = get_items(extraParameters="?page=1&pageSize=50&sortBy=date&sortOrder=desc")
    item_list = json.loads(r.text)
    date_list = []
    for elem in item_list:
        date_list.append(int(elem[1].replace("-", "")))
    # check if list is sorted in descending order
    assert all(earlier >= later for earlier, later in zip(date_list, date_list[1:]))

def test_filtering():
    filter_state = "running"
    r = get_items(extraParameters="?page=1&pageSize=50&filterField=state&filterValue={filter_state}")
    item_list = json.loads(r.text)
    date_list = []
    for elem in item_list:
        if elem[2] != filter_state:
            assert False
    assert True

def test_queryInvalidParameters():
    
    r = get_items(extraParameters="?page=1&pageSize=500000000000000000000000000000000000")
    assert r.status_code == 500

    r = get_items(extraParameters="?page=1&pageSize=50&nuff=asd")
    assert r.status_code == 200


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
