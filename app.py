from flask import Flask, json, request, jsonify, redirect, url_for

import random, string, sqlite3


api = Flask(__name__)

# mocking static User DB
user_db = [
    {
        "uid": 1,
        "username": "usr1",
        "password": "pass1",
        "allowed_items": [
            "item1",
            "item2",
            "item4"
            ]
    },
    {
        "uid": 2,
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
cur.execute("CREATE TABLE IF NOT EXISTS items (item_id, date, state, user_id)")

itemlist = [
        #[item_id, date, state, userid]
        ("item1","2021-10-16","stopped", "1"),
        ("item2","2021-10-18","paused", "1"),
        ("item3","2021-11-19","running", "2"),
        ("item4","2021-11-16","paused", "2"),
        ("item5","2021-11-17","stopped", "1"),
        ("item6","2021-11-18","running", "0"),
]
cur.executemany("insert into items values (?, ?, ?, ?)", itemlist)


# mocking user session
class UserSession(object):
    
    def __init__(self):
        # super().__init__()
        self.session_token = ""
        self.view = "login"
        self.user = ""
        self.password = ""
        self.uid = 0
        self.session_token = ""
        self.allowed_items = []

    # @staticmethod
    def check_credentials(self, creds):
        for elem in user_db:
            if (creds["username"] == elem["username"]) and \
            (creds["password"] == elem["password"]):
                self.user = elem["username"]
                self.allowed_items = elem["allowed_items"]
                self.password = elem["password"]
                self.uid = elem["uid"]
                return True
        return False

    def replace_user_data(self, new_data):
        something_changed = False
        for elem in user_db:
            if self.uid == elem["uid"]:
                for key in new_data.keys():
                    if (new_data[key] and new_data[key] != elem[key]):
                        elem[key] = new_data[key]
                        something_changed = True
        return something_changed

    def invalidate_token(self):
        self.session_token = ""
        self.user = ""
        self.view = "login"

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
    
    print("---dbg---")
    print(page, page_size, sortby, order, filter_field, filter_value)

    if (filter_field == "any"):
        sql_query = "SELECT * FROM items ORDER BY {} {} LIMIT {}".format(sortby, order, str(page_size))
    else:
        sql_query = "SELECT * FROM items WHERE {} = '{}' ORDER BY {} {} LIMIT {}".format(filter_field, filter_value, sortby, order, str(page_size))
    cur.execute(sql_query)
    return cur.fetchall()


@api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        usr.view = "login"
        return json.dumps({"state": usr.view})
    else:
        content = request.get_json()
        if usr.check_credentials(content):
            session_token = usr.generate_session_token()
            usr.view = "dashboard"
            # print("----")
            # print(usr.view)
            # print(usr.uid)
            # print(usr.user)
            # print(usr.password)
            # print(usr.allowed_items)
            response = json.dumps({"success": True, "message": "Login successful!", "session_token": session_token, "state": usr.view }), 200
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
        return json.dumps({"success": True, 
                           "message": "Dashboard loaded,",
                           "session_token": auth_token,
                           "logged_user": usr.user,
                           "state": usr.view}), 200

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

        items = get_list_of_items(page,page_size, sort_by, sort_order, filter_field, filter_value)
        return jsonify(items), 200

    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401


@api.route('/config', methods=["GET", "PUT"])
def config():
    auth_token = request.headers.get('Authorization')
    if usr.valid_token(auth_token):
        # sets the state/view to config
        if request.method == "GET":
            usr.view = "config"
            return json.dumps({"success": True,
                    "message": "Config loaded,",
                    "session_token": auth_token,
                    "state": usr.view,
                    "user": usr.user,
                    "password": usr.password,
                    "uid": usr.uid,
                    "token": usr.session_token,
                    "allowed_items": usr.allowed_items}), 200
        else:
            # PUT
            print(request.data)
            print(json.loads(request.data.decode()))
            usr.replace_user_data(json.loads(request.data.decode()))
            usr.invalidate_token()
            # redirect flow:
            # change the state
            # do a redirect
            return json.dumps({"success": True, "message": "Modified configuration for user {}. Consider redirection.".format(usr.user),
                 "session_token": auth_token, "user": usr.user, "state": usr.view }), 200
    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401


@api.route('/items/<item_id>/details', methods=["GET"])
def get_item_details(item_id):
    auth_token = request.headers.get('Authorization')
    if usr.valid_token(auth_token):
        # sets the state/view to config
        if request.method == "GET":
            usr.view = "item_details"
            cur.execute("select * from items where item_id=(?)", (item_id, ))
            item  = cur.fetchone()
            if item: 
                return jsonify({"item": item, "state": usr.view}), 200
            
            return json.dumps({"success": False, "message": "Item not found.", "state": usr.view}), 404

    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401

#TODO move out the item states in a class/enum
valid_item_states = ("running", "paused", "stopped")


@api.route('/items/<item_id>', methods=["PUT"])
def update_item_state(item_id):
    auth_token = request.headers.get('Authorization')
    if usr.valid_token(auth_token):
        if request.method == "PUT":
            content = request.get_json()
            
            if content["state"] not in valid_item_states:
                return json.dumps({"success": False, "message": "Invalid item state." }), 400

            cur.execute("select * from items where item_id=(?)", (item_id, ))
            item  = cur.fetchone()
            if item:
                if item[0] in usr.allowed_items:
                    cur.execute("UPDATE items SET state = ? where item_id=?", (str(content["state"]),str(item_id)))
                    usr.view = "item_control"
                    return json.dumps({"success": True, "message": "State updated.", "state": usr.view }), 200
                else:
                    return json.dumps({"success": False, "message": "State change not allowed." }), 403

            return json.dumps({"success": False, "message": "Item not found." }), 404

    return json.dumps({"success": False, "message": "Unauthorized.", "session_token": auth_token }), 401


if __name__ == '__main__':
    api.run()
