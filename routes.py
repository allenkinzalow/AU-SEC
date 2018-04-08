from flask import jsonify, request, render_template, jsonify, make_response, request, abort, Blueprint
from models import Authorizer_User, Policy, Patient
from dispatch.Dispatcher import Dispatcher
from crafter import craftQuery
from database import db_session
from config import DEFAULT_DATA_TABLE
routes = Blueprint('routes', __name__, template_folder='templates')

def check_json(json, *params):
    if not json:
        return False
    for key in params:
        if not key in json:
            return False
    return True

@routes.route('/')
def index():
    return render_template('index.html')

# {preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@routes.route('/api/auth_users/create_user', methods=['POST'])
def create_user():
    if not check_json(request.json, 'preferred_comms', 'contact_info'):
        abort(400)
    user = Authorizer_User(request.json['preferred_comms'], request.json['contact_info'])
    db_session.add(user)
    db_session.commit()
    return make_response(jsonify({"auth_id": user.auth_id}), 200)

# {auth_id: id, preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@routes.route('/api/auth_users/edit_user', methods=['PUT'])
def edit_user():
    if not check_json(request.json, 'auth_id', 'preferred_comms', 'contact_info'):
        abort(400)

    user = Authorizer_User.query.get(request.json['auth_id'])
    user.preferred_comms = int(request.json['preferred_comms'])
    user.contact_info = request.json['contact_info']
    db_session.commit()
    return make_response(jsonify({"auth_id": user.auth_id, "status": "success"}), 200)

# {data_id: id, authorizers: [id1, id2, ...], column_name: name, table_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
# Policy bitwise: 6 bits indicating on/off for notification/authorization of delete/update/select
@routes.route('/api/policies/create_policy', methods=['POST'])
def create_policy():
    if not check_json(request.json, 'data_id', 'authorizers', 'policy_bitwise'):
        abort(400)
    if not 'table_name' in request.json:
        request.json['table_name'] = DEFAULT_DATA_TABLE
    if not 'expiration' in request.json:
        request.json['expiration'] = 'NULL'
    if 'column_name' in request.json:
        policy = Policy(request.json['data_id'], request.json['authorizers'], request.json['column_name'], request.json['table_name'], request.json['expiration'], request.json['policy_bitwise'])
        db_session.add(policy)
        db_session.commit()
        return make_response(jsonify({'policy_id': policy.policy_id, 'status': 'success'}), 200)
    else:
        data = Patient.query.get(request.json['data_id'])
        for c in data.columns:
            print(c)
    return

# {data_id: id, authorizers: [id1, id2, ...], column_name: name, table_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
@routes.route('/api/policies/edit_policy', methods=['PUT'])
def edit_policy():
    if not check_json(request.json, 'data_id', 'authorizers', 'policy_bitwise'):
        abort(400)
    return

#{data: {column_names: column_data}, table_name: table, authorized_user: auth_id, row_id: id}
@routes.route('/api/data/update', methods=['PUT'])
def update_data():
    
    query_dict = {"row_id":request.json["row_id"], "table_name":request.json["table_name"],
                  "columns":request.json["new_data"].keys(),
                  "values":list(request.json["new_data"].values())}
    SQL_query,SQL_values = craftQuery(query_dict)    
    return 

# {row_id: id, table_name: table, data: {column_name: "", }}
@routes.route('/api/data/select', methods=['PUT'])
def select_data():
    if data in request.json:
        query_dict = {"columns":request.json["data"].keys()
    query_dict["table_name"] = request.json["table_name"]
    query_dict["row_id"] = request.json["row_id"]
    #the value returned here is a single item list containing the row_id
    SQL_query,SQL_values = craftQuery(query_dict)
    return SQL_query


# {data: {column_names: column_data}, table_name: table, authorized_user: id}
@routes.route('/api/data/insert', methods=['POST'])
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
@routes.route('/api/data/delete', methods=['PUT'])
def delete_data():
    if not check_json(request.json, 'row_id'):
        abort(400)
    query_dict = dict(request.json)
    #the value returned here is a single item list containing the row_id
    SQL_query,SQL_values = craftQuery(query_dict)
    return SQL_query

@routes.route('/api/data/view_history', methods=[''])
def view_data_history():    
    return

@routes.route('/api/dispatch/send')
def send_auth_reqiest():
    return

@routes.route('/api/dispatch/receive')
def get_auth_update():
    return
