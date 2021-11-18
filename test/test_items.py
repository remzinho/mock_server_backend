from helpers.utils import *
import pytest


def test_getItemDetails():
    """
    Tests simple dashboard calls.
    """
    token = get_auth_token("usr1", "pass1")
    r = get_item_details("item1", token)
    assert r.status_code == 200
    check_property_in_response(r, "state", "item_details")
    item_list = [
        "item1",
        "2021-10-16",
        "stopped",
        "1"
    ]
    check_property_in_response(r, "item", item_list)

def test_getInvalidItemDetails():
    """
    Tests simple dashboard calls.
    """
    token = get_auth_token("usr1", "pass1")
    # item0 should be invalid
    r = get_item_details("item0", token)
    assert r.status_code == 404
    check_property_in_response(r, "message", "Item not found.")


def change_item_and_validate(new_state, item_list):
    token = get_auth_token("usr1", "pass1")
    new_value = new_state
    r = update_item_details("item1", new_value, token)
    r = get_item_details("item1", token)

    check_property_in_response(r, "item", item_list)

def test_changeItemState():
    item_list = [
        "item1",
        "2021-10-16",
        "running",
        "1"
    ]
    change_item_and_validate("running", item_list)

    item_list[2] = "stopped"

    # change it back ("cleanup")
    change_item_and_validate("stopped", item_list)

def test_unauthorizedStateChange():
    token = get_auth_token("usr1", "pass1")
    new_value = "stopped"
    # item6 was defined to be inaccesible by any of the 2 users
    r = update_item_details("item6", new_value, token)
    assert r.status_code == 403
    check_property_in_response(r, "message", "State change not allowed.")
