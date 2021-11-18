from flask import Flask, json, request, jsonify, redirect, url_for
import random, string, sqlite3


api = Flask(__name__)

# mocking static User DB
user_db = [
    {
        "username": "usr1",
        "password": "pass1",
        "allowed_items": [
            "item1",
            "item2",
            "item4"
            ]
    },
    {
        "username": "usr2",
        "password": "pass2",
        "allowed_items": [
            "item4",
            "item5",
            "item6"
            ]
    }
]

# mock sqlite db
con = sqlite3.connect(":memory:", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS items (item_id, date, state)")

itemlist = [
        ("item1","2021-10-16","stopped"),
        ("item2","2021-10-18","paused"),
        ("item3","2021-11-19","running"),
        ("item4","2021-11-16","paused"),
        ("item5","2021-11-17","stopped"),
        ("item6","2021-11-18","running"),
]
cur.executemany("insert into items values (?, ?, ?)", itemlist)


# mocking user session
class UserSession(object):
    
    def __init__(self):
        # super().__init__()
        self.session_token = ""
        self.view = "login"

    @staticmethod
    def check_credentials(creds):
        for elem in user_db:
            if (creds["username"] == elem["username"]) and \
            (creds["password"] == elem["password"]):
                return True
        return False

    def generate_session_token(self):
        letters = string.ascii_lowercase
        tmp_rand_str =  ''.join(random.choice(letters) for i in range(10))
        self.session_token = tmp_rand_str
        return tmp_rand_str

    def valid_token(self, token):
        if token == self.session_token and self.session_token != "":
            return True
        return False


views = [
    "login",
    "dashboard",
    "config",
    "item_details",
    "item_control"
    ]

usr = UserSession()


def get_list_of_items(page, page_size, sortby, order, filter_field, filter_value):
    
    print("------")
    print(page, page_size, sortby, order, filter_field, filter_value)

    if (filter_field == "any"):
        sql_query = "SELECT * FROM items ORDER BY {} {} LIMIT {}".format(sortby, order, str(page_size))
    else:
        sql_query = "SELECT * FROM items WHERE {} = '{}' ORDER BY {} {} LIMIT {}".format(filter_field, filter_value, sortby, order, str(page_size))
    cur.execute(sql_query)
    print(cur.fetchall())


@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        current_view = {"state": "login"}
        return json.dumps(current_view)
    else:
        content = request.get_json()
        if usr.check_credentials(content):
            session_token = usr.generate_session_token()
            response = json.dumps({"success": True, "message": "Login successful!", "session_token": session_token }), 200
            # not doing redirect here; this will be done in frontend, as well as the auth token
            # response = redirect(url_for("dashboard"), code=200)
            # response.headers = {'Authorization': session_token}
        else:
            response = json.dumps({"success": False, "message": "Wrong username/password!"}), 401
        return response
    

@api.route('/dashboard', methods=["GET"])
def dashboard():
    auth_token = request.headers.get('Authorization')
    
    if usr.valid_token(auth_token):
        # sets the state/view to dashboard
        usr.view = "dashboard"
        return json.dumps({"success": True, "message": "Dashboard loaded,", "session_token": auth_token }), 200
    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401

@api.route('/items', methods=["GET"])
def get_items():
    auth_token = request.headers.get('Authorization')
    if usr.valid_token(auth_token):

        page         = request.args.get('page', default=1, type=int)
        page_size    = request.args.get('pageSize', default=5, type=int)
        sort_by     = request.args.get('sortBy', default="date", type=str)
        sort_order   = request.args.get('sortOrder', default="asc", type=str)
        filter_field = request.args.get('filterField', default="any", type=str)
        filter_value = request.args.get('filterValue', default="any", type=str)

        get_list_of_items(page,page_size, sort_by, sort_order, filter_field, filter_value)

        return json.dumps({"success": True, "message": "Got list of items", "session_token": auth_token }), 200
    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401


@api.route('/config', methods=["GET", "PUT"])
def config():
    auth_token = request.headers.get('Authorization')
    if usr.valid_token(auth_token):
        # sets the state/view to config
        if request.method == "GET":
            usr.view = "config"
            return json.dumps({"success": True, "message": "Config loaded,", "session_token": auth_token }), 200
        else:

    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401


if __name__ == '__main__':
    api.run()
