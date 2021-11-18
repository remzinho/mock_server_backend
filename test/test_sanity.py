from helpers.login_utils import *


def test_serverUp():
    """
    Tests if the server it up and running
    """
    r = requests.get(globals.urls["login"])
    assert r.status_code == 200

    r = requests.get(globals.urls["host"])
    assert r.status_code == 404
