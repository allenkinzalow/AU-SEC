from app import app
from flask import jsonify, request, render_template, jsonify, make_response, request, abort
from models import Authorizer_User
from dispatch.Dispatcher import Dispatcher
from crafter import craftQuery

def check_json(json, *params):
    if not json:
        return False
    for key in params:
        if not key in json:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

# {preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@app.route('/api/auth_users/create_user', methods=['POST'])
def create_user():
    if not check_json(request.json, 'preferred_comms', 'contact_info'):
        abort(400)
    user = {
        'id': generate_uuid(),
        'preferred_comms': request.json['preferred_comms'],
        'contact_info': request.json['contact_info']
    }

    # Database stuff here

    return make_response(jsonify({"id": user['id']}), 200)

# {user_id: id, preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@app.route('/api/auth_users/edit_user', methods=['PUT'])
def edit_user():
    if not check_json(request.json, 'user_id', 'preferred_comms', 'contact_info'):
        abort(400)

    # Database stuff here
    return

# {data_id: id, authorizers: [id1, id2, ...], column_name: name, table_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
# Policy bitwise: 6 bits indicating on/off for notification/authorization of delete/update/select
@app.route('/api/policies/create_policy', methods=['POST'])
def create_policy():
    if not check_json(request.json, 'data_id', 'authorizers', 'policy_bitwise'):
        abort(400)
    return

# {data_id: id, authorizers: [id1, id2, ...], column_name: name, table_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
@app.route('/api/policies/edit_policy', methods=['PUT'])
def edit_policy():
    if not check_json(request.json, 'data_id', 'authorizers', 'policy_bitwise'):
        abort(400)
    return

# {row_id: id, table_name: table, new_data: {column_name: column, ...}}
@app.route('/api/data/update', methods=['PUT'])
def update_data():
    
    query_dict = {"row_id":request.json["row_id"], "table_name":request.json["table_name"],
                  "columns":request.json["new_data"].keys(),
                  "values":list(request.json["new_data"].values())}
    SQL_query,SQL_values = craftQuery(query_dict)    
    return 

# {row_id: id, table_name: table, data: {column_name: "", }}
@app.route('/api/data/select', methods=['PUT'])
def select_data():
    if data in request.json:
        query_dict = {"columns":request.json["data"].keys()
    query_dict["table_name"] = request.json["table_name"]
    query_dict["row_id"] = request.json["row_id"]
    #the value returned here is a single item list containing the row_id
    SQL_query,SQL_values = craftQuery(query_dict)
    return SQL_query

# {data: {column_names: column_data}, table_name: table, authorized_user: auth_id, row_id: id}
@app.route('/api/data/insert', methods=['POST'])
def insert_data():
    if not check_json(request.json, 'authorized_user', 'data'):
        abort(400)
    columns = request.json["data"].keys()
    values = list(request.json["data"].values())
    query_dict = {"columns":columns,"values":values,
                  "table_name":request.json["table_name"], 
                  "row_id":request.json["row_id"],
                  "auth_id":request.json["auth_id"]}
    SQL_query,SQL_values = craftQuery(query_dict)
    return SQL_query

# {row_id: id, table_name: table}
@app.route('/api/data/delete', methods=['PUT'])
def delete_data():
    if not check_json(request.json, 'row_id'):
        abort(400)
    query_dict = dict(request.json)
    #the value returned here is a single item list containing the row_id
    SQL_query,SQL_values = craftQuery(query_dict)
    return SQL_query

@app.route('/api/data/view_history', methods=[''])
def view_data_history():    
    return

@app.route('/api/dispatch/send')
def send_auth_reqiest():
    return

@app.route('/api/dispatch/receive')
def get_auth_update():
    return
