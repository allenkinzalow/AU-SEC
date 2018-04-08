from flask import jsonify, request, render_template, jsonify, make_response, request, abort, Blueprint
from models import *
from dispatch.Dispatcher import Dispatcher
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
        abort(400, {'message': 'Essential json keys not found (preferred_comms, contact_info)'})
    user = Authorizer_User(request.json['preferred_comms'], request.json['contact_info'])
    db_session.add(user)
    db_session.commit()
    return make_response(jsonify({"auth_id": user.auth_id}), 200)

# {auth_id: id, preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@routes.route('/api/auth_users/edit_user', methods=['POST'])
def edit_user():
    if not check_json(request.json, 'auth_id', 'preferred_comms', 'contact_info'):
        abort(400, {'message': 'Essential json keys not found (auth_id, preferred_comms, contact_info)'})

    user = Authorizer_User.query.get(request.json['auth_id'])
    user.preferred_comms = int(request.json['preferred_comms'])
    user.contact_info = request.json['contact_info']
    db_session.commit()
    return make_response(jsonify({"auth_id": user.auth_id, "status": "success"}), 200)

def create_auth_group(authorizers):
    """ Helper function to create an authorization group and populate the rows in groups table """
    group_id = generate_uuid()
    for auth_id in authorizers:
        g = Group(auth_id, group_id)
        db_session.add(g)
    return group_id

# {data_id: id, authorz`izers: [id1, id2, ...], column_name: name, table_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
# Policy bitwise: 6 bits indicating on/off for notification/authorization of delete/update/select
@routes.route('/api/policies/create_policy', methods=['POST'])
def create_policy():

    policy_ids, group_ids = [], []

    if not check_json(request.json, 'data_id', 'authorizers', 'policy_bitwise'):
        abort(400, {'message': 'Essential json keys not found (data_id, authorizers, policy_bitwise)'})

    data = Patient.query.get(request.json['data_id'])
    if not data:
        abort(400, {'message': 'The data_id provided did not return any data'})

    if not 'table_name' in request.json:
        request.json['table_name'] = DEFAULT_DATA_TABLE
    if not 'expiration' in request.json:
        request.json['expiration'] = 'NULL'
    if 'column_name' in request.json:
        policy = Policy(request.json['data_id'], request.json['authorizers'], request.json['column_name'], request.json['table_name'], request.json['expiration'], request.json['policy_bitwise'])
        db_session.add(policy)
        policy_ids.append(policy.policy_id)
        group_ids.append(create_auth_group(request.json['authorizers']))
    else:
        for col in Patient.__table__.columns.keys():
            policy = Policy(request.json['data_id'], request.json['authorizers'], col, request.json['table_name'], request.json['expiration'], request.json['policy_bitwise'])
            db_session.add(policy)
            policy_ids.append(policy.policy_id)
            group_ids.append(create_auth_group(request.json['authorizers']))

    db_session.commit()
    return make_response(jsonify({'policy_ids': policy_ids, 'group_ids': group_ids, 'status': 'success'}), 200)

# {policy_ids: [id1m id2, ...], authorizers: [id1, id2, ...], column_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
@routes.route('/api/policies/edit_policy', methods=['POST'])
def edit_policy():
    if not check_json(request.json, 'policy_ids'):
        abort(400, {'message': 'Essential json keys not found (policy_ids)'})
    policies = Policy.query.filter(Policy.policy_id.in_(request.json['policy_ids'])).all()
    if not policies:
        abort(400, {'message': 'No policies with those ids exist'})
    for policy in policies:
        if 'expiration' in request.json:
            policy.experiation = request.json['experiation']
        if 'policy_bitwise' in request.json:
            policy.policy_bitwise = request.json['policy_bitwise']
        if 'column_name' in request.json:
            policy.column_name = request.json['column_name']
        if 'authorizers' in request.json:
            old_group_id = policy.group_id
            policy.group_id = create_auth_group(request.json['authorizers'])
            Group.query.filter_by(group_id == old_group_id).delete()
    db_session.commit()
    return make_response(jsonify({'policy_ids': request.json['policy_ids'], 'status': 'success'}), 200)

# {row_id: id, new_data: {column_name: column, ...}}
@routes.route('/api/data/update', methods=['PUT'])
def update_data():    
    return

# {data: {column_name: "", ...}, table_name}
@routes.route('/api/data/select', methods=['PUT'])
def select_data():    
    return

# {data: {column_names: column_data}, table_name: table, authorized_user: id}
@routes.route('/api/data/insert', methods=['POST'])
def insert_data():
    if not check_json(request.json, 'authorized_user', 'data'):
        abort(400)

    return

# {row_id: id, table_name: table}
@routes.route('/api/data/delete', methods=['PUT'])
def delete_data():
    if not check_json(request.json, 'row_id'):
        abort(400)
    return

@routes.route('/api/data/view_history', methods=[''])
def view_data_history():    
    return

@routes.route('/api/dispatch/send')
def send_auth_reqiest():
    return

@routes.route('/api/dispatch/receive')
def get_auth_update():
    return