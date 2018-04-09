from flask import jsonify, request, render_template, jsonify, make_response, request, abort, Blueprint
from models import *
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

@routes.route('/api/patients', methods=['GET'])
def get_all_patients():
    patients = Patient.query.all()
    return jsonify([p.get_object() for p in patients])

# {preferred_comms: <integer>{1,2,3}, contact_info: <string>, name: name}
@routes.route('/api/auth_users/create_user', methods=['POST'])
def create_user():
    if not check_json(request.json, 'preferred_comms', 'contact_info', 'name'):
        abort(400, {'message': 'Essential json keys not found (preferred_comms, contact_info, name)'})
    user = Authorizer_User(request.json['preferred_comms'], request.json['contact_info'], request.json['name'])
    db_session.add(user)
    db_session.commit()
    return make_response(jsonify({"auth_id": user.auth_id}), 200)

# {auth_id: id, preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@routes.route('/api/auth_users/edit_user', methods=['POST'])
def edit_user():
    if not check_json(request.json, 'auth_id'):
        abort(400, {'message': 'Essential json keys not found (auth_id)'})

    user = Authorizer_User.query.get(request.json['auth_id'])
    if 'preferred_comms' in request.json:
        user.preferred_comms = int(request.json['preferred_comms'])
    if 'contact_info' in request.json:
        user.contact_info = request.json['contact_info']
    if 'name' in request.json:
        user.name = request.json['name']
    db_session.commit()
    return make_response(jsonify({"auth_id": user.auth_id, "status": "success"}), 200)

# {name: name}
@routes.route('/api/auth_users/get_user', methods=['POST'])
def get_user():
    if not check_json(request.json, 'name'):
        abort(400, {'message': 'Essential json keys not found (name)'})

    users = Authorizer_User.query.filter(Authorizer_User.name == request.json['name']).all()
    return make_response(jsonify({'auth_users': [user.get_object() for user in users]}))

def create_auth_group(authorizers):
    """ Helper function to create an authorization group and populate the rows in groups table """
    group_id = generate_uuid()
    for auth_id in authorizers:
        g = Group(auth_id, group_id)
        db_session.add(g)
    return group_id

# {data_id: id, authorizers: [id1, id2, ...], column_name: name, table_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
# Policy bitwise: 6 bits indicating on/off for notification/authorization of delete/update/select
@routes.route('/api/policies/create_policy', methods=['POST'])
def create_policy():

    policy_ids, group_ids = [], []

    if not check_json(request.json, 'data_id', 'authorizers', 'policy_bitwise'):
        abort(400, {'message': 'Essential json keys not found (data_id, authorizers, policy_bitwise)'})

    data = Patient.query.get(request.json['data_id'])
    if not data:
        abort(400, {'message': 'The data_id provided did not return any policies'})

    if not 'table_name' in request.json:
        request.json['table_name'] = DEFAULT_DATA_TABLE
    if not 'expiration' in request.json:
        request.json['expiration'] = 'NULL'
    if 'column_name' in request.json:
        group_id = create_auth_group(request.json['authorizers'])
        policy = Policy(request.json['data_id'], request.json['authorizers'], group_id, request.json['column_name'], request.json['table_name'], request.json['expiration'], request.json['policy_bitwise'])
        db_session.add(policy)
        policy_ids.append(policy.policy_id)
    else:
        group_id = create_auth_group(request.json['authorizers'])
        for col in Patient.__table__.columns.keys():
            policy = Policy(request.json['data_id'], request.json['authorizers'], group_id, col, request.json['table_name'], request.json['expiration'], request.json['policy_bitwise'])
            db_session.add(policy)
            policy_ids.append(policy.policy_id)

    group_members = []
    for auth_id in request.json['authorizers']:
        auth_user = Authorizer_User.query.get(auth_id)
        group_members.append(auth_user.get_object())

    db_session.commit()
    return make_response(jsonify({'policy_ids': policy_ids, 'group_id': group_id, 'group_members': group_members, 'status': 'success'}), 200)

# {policy_ids: [id1, id2, ...], authorizers: [id1, id2, ...], column_name: name, expiration: datetime, policy_bitwise: <6 bit integer>}
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

# {policy_ids: [id1, id2, ...], auth_ids: [id1, id2, ...], data_ids: [id1, id2, ...], column_names: [column1, column2, ...]}
@routes.route('/api/policies/get_policies', methods=['POST'])
def get_policies():
    if 'policy_ids' in request.json:
        policies = Policy.query.filter(Policy.policy_id.in_(request.json['policy_ids'])).all()
    elif 'auth_ids' in request.json:
        groups = Group.query.filter(Group.auth_id.in_(request.json['auth_ids'])).all()
        group_ids = [group.group_id for group in groups]
        policies = Policy.query.filter(Policy.group_id.in_(group_ids)).all()
    elif 'data_ids' in request.json:
        policies = Policy.query.filter(Policy.data_id.in_(request.json['data_ids'])).all()
    else:
        abort(400, {'message': 'One of (policy_ids, auth_ids, data_ids) needed'})
    if not policies:
        return make_response(jsonify({'policies': [], 'status': 'error'}))
    if 'column_names' in request.json:
        policies = [policy.get_object() for policy in policies if policy.column_name in request.json['column_names']]
    else:
        policies = [policy.get_object() for policy in policies]
    for policy in policies:
        groups = Group.query.filter(Group.group_id == policy['group_id']).all()
        auth_ids = [group.auth_id for group in groups]
        group_members = []
        for auth_id in auth_ids:
            auth_user = Authorizer_User.query.filter(Authorizer_User.auth_id == auth_id).first()
            if auth_user:
                group_members.append(auth_user.get_object())
        policy['group_members'] = group_members

    return make_response(jsonify({'policies': policies, 'status': 'success'}))

def create_pending_policy(policy_id, sql_query, expiration):
    auth_group_id = generate_uuid()
    pending_policy = Pending_Policy(policy_id, sql_query, expiration, auth_group_id)
    db_session.add(pending_policy)
    policy = Policy.query.filter(Policy.policy_id == policy_id).first()
    auth_ids = Group.query.filter(Group.group_id == policy.group_id).all()
    auth_ids = [user.auth_id for user in auth_ids]
    auth_users = Authorizer_User.query.filter(Authorizer_User.auth_id.in_(auth_ids))
    print(auth_users)
    for user in auth_users:
        print(user)
        # Authy authorization
        if int(user.preferred_comms) == 1:
            uuid, authy_auth_id = send_auth_request(user.auth_id, int(user.contact_info), "Would you like to allow access to this data?", 60, {})
        pending_auth = Pending_Auth(user.auth_id, auth_group_id, uuid)
        db_session.add(pending_auth)
    db_session.commit()

#{data: {column_names: column_data}, table_name: table, data_id: id}
@routes.route('/api/data/update', methods=['POST'])
def update_data():
    if not check_json(request.json, 'data_id', 'data'):
        abort(400, {'message': 'Essential json keys not found (data_id, data)'})
    policy_bitwise = '000000'
    policy = Policy.query.filter(Policy.data_id == request.json['data_id']).first()
    if policy:
        policy_bitwise = "{0:b}".format(policy.policy_bitwise).zfill(6)
    if int(str(policy_bitwise)[0]):
        if not 'table_name' in request.json:
            request.json['table_name'] = DEFAULT_DATA_TABLE
        query_dict = {"command":"update","data_id":request.json["data_id"], "table_name":request.json["table_name"],
                      "columns":request.json["data"].keys(),
                      "values":list(request.json["data"].values())}
        SQL_query = craftQuery(query_dict)    
        print(SQL_query)
        
        create_pending_policy(policy.policy_id, SQL_query, policy.expiration)

        print("NEEDS AUTH")   
        return make_response(jsonify({'status': 'pending'}))

    if int(str(policy_bitwise)[1]):
        print("NEED NOTIFY")

    patient = Patient.query.get(request.json['data_id'])
    if 'name' in request.json['data']:
        patient.name = request.json['data']['name']
    if 'medicine' in request.json['data']:
        patient.medicine = request.json['data']['medicine']
    if 'amount' in request.json['data']:
        patient.amount = request.json['data']['amount']
    db_session.commit()
    return make_response(jsonify({'patient': patient.get_object(), 'status': 'success'}))

# {data_id: id, table_name: table, data: {column_name: "", }}
@routes.route('/api/data/select', methods=['POST'])
def select_data():
    policy_bitwise = '000000'
    policy = None
    if 'data_id' in request.json:
        policy = Policy.query.filter(Policy.data_id == request.json['data_id']).first()
    if policy:
        policy_bitwise = "{0:b}".format(policy.policy_bitwise).zfill(6)
    if int(str(policy_bitwise)[4]):
        query_dict = {"command":"select"}
        if "data" in request.json:
            query_dict = {"columns":request.json["data"].keys()}
        if not 'table_name' in request.json:
            request.json['table_name'] = DEFAULT_DATA_TABLE
        query_dict["table_name"] = request.json["table_name"]
        if 'data_id' in request.json:
            query_dict["data_id"] = request.json["data_id"]
        else:
            query_dict['data_id'] = '*'
        #the value returned here is a single item list containing the data_id
        SQL_query = craftQuery(query_dict)
        
        create_pending_policy(policy.policy_id, SQL_query, policy.expiration)
        print("NEEDS AUTH")
        return make_response(jsonify({'status': 'pending'}))
    
    if int(str(policy_bitwise)[5]):
        print("NEED NOTIFY")

    if 'data_id' in request.json:
        patient = Patient.query.get(request.json['data_id'])
        data = {}
        if 'data' in request.json:
            for key in patient.get_object().keys():
                if key in request.json['data']:
                    data[key] = patient.get_objects[key]
        else:
            data = patient.get_object()
        return make_response(jsonify({'status': 'success', 'patients': [data]}))
    patients = Patient.query.all()
    if 'data' in request.json:
        if 'medicine' in request.json['data']:
            patients = [patient for patient in patients if patient.medicine == request.json['data']['medicine']]
        if 'amount' in request.json['data']:
            patients = [patient for patient in patients if patient.amount == request.json['data']['amount']]
        if 'name' in request.json['data']:
            patients = [patient for patient in patients if patient.name == request.json['data']['name']]
    patients = [patient.get_object() for patient in patients]
    return make_response(jsonify({'status': 'success', 'patients': patients}))


# {data: {column_names: column_data}, table_name: table, auth_id: auth_id}
@routes.route('/api/data/insert', methods=['POST'])
def insert_data():
    if not check_json(request.json, 'auth_id', 'data'):
        abort(400)
    patient = Patient(request.json['data']['name'], request.json['auth_id'], request.json['data']['medicine'], request.json['data']['amount'])
    db_session.add(patient)
    db_session.commit()
    return make_response(jsonify({'data_id': patient.data_id, 'auth_id': patient.auth_id, 'status': 'success'}))

# {data_id: id, table_name: table}
@routes.route('/api/data/delete', methods=['POST'])
def delete_data():
    if not check_json(request.json, 'data_id'):
        abort(400)
    policy_bitwise = '000000'
    policy = Policy.query.filter(Policy.data_id == request.json['data_id']).first()
    if policy:
        policy_bitwise = "{0:b}".format(policy.policy_bitwise).zfill(6)

    # Needs authorization
    if int(str(policy_bitwise)[2]):
        # Build query to keep in table
        query_dict = dict(request.json)
        query_dict["command"] = "delete"
        # the value returned here is a single item list containing the data_id
        SQL_query = craftQuery(query_dict)
        create_pending_policy(policy.policy_id, SQL_query, policy.expiration)

        print("NEEDS AUTH")   
        return make_response(jsonify({'status': 'pending'}))

    # Needs notify
    if int(str(policy_bitwise)[3]):
        print("NEEDS NOTIFY")

    # Go ahead and delete
    patient = Patient.query.filter(Patient.data_id == request.json['data_id']).delete()
    db_session.commit()
    return make_response(jsonify({'status': 'success'}))

def send_auth_request(auth_id, authy_user_id, message, time_limit, details):
    pusher = Dispatcher()
    uuid, authy_auth_id = pusher.oneTouchAuth(auth_id, authy_user_id, message, time_limit, details)
    return uuid, authy_auth_id

@routes.route('/api/dispatch/send')
def send_auth_request_api():
    if not check_json(request.json, 'authorization_id', 'authy_user_id', 'message', 'time_Limit', 'details'):
        abort(400)
    uuid, authy_auth_id = send_auth_request(request.json['authorization_id'], request.json['authy_user_id'], request.json['message'], request.json['time_Limit'], request.json['details'])
    return make_response(jsonify({'uuid': uuid, 'authy_auth_id': authy_auth_id}))

@routes.route('/api/dispatch/receive', methods=['POST'])
def get_auth_update():
    ##Assuming the POST becomes the request.json. JSON key names are correct in any event.
    print(request.json)
    receive_uuid = request.json['uuid']
    receive_auth_id = request.json['approval_request']['transaction']['hidden_details']['auth_id']
    status = request.json['status'].strip()
    pending_auths = Pending_Auth.query.filter(Pending_Auth.auth_id == receive_auth_id).all()
    pending_auth = [pending_auth for pending_auth in pending_auths if pending_auth.comms_info == str(receive_uuid)][0]
    print(pending_auth)
    if status == 'approved':
        db_session.delete(pending_auth)
        needed_auths = Pending_Auth.query.filter(Pending_Auth.group_id == pending_auth.group_id).all()
        print(needed_auths)
        if needed_auths:
            print("RUN THE COMMAND")
            pending_policy = Pending_Policy.query.filter(Pending_Policy.auth_group_id == pending_auth.group_id).first()
            print(pending_policy.command)
            db_session.execute(pending_policy.command)
    elif status == 'denied':
        # find pending policy and drop
        Pending_Policy.query.filter(Pending_Policy.auth_group_id == pending_auth.group_id).delete()
        Pending_Auth.query.filter(Pending_Auth.group_id == pending_auth.group_id).delete()
    #else if status == 'expired':
    else:
        # find pending policy and drop for now
        Pending_Policy.query.filter(Pending_Policy.auth_group_id == pending_auth.group_id).delete()
        Pending_Auth.query.filter(Pending_Auth.group_id == pending_auth.group_id).delete()  
    
    ##Use uuid to determine which pending policy the result applies to and make changes (or don't) accordingly. 
    ##Similar to send_auth_req, probably aren't going to be returning the uuid/auth_result, just placeholding for now.
    db_session.commit()
    return make_response(jsonify({'uuid': receive_uuid, 'status': 'success'}))

@routes.route('/api/history/<data_id>', methods=['GET'])
def get_history(data_id):
    entries = History.query.filter(History.data_id==data_id)
    return jsonify([e.get_object() for e in entries])

# {data_id: id, table_name: table}
@routes.route('/api/data/deadman', methods=['POST'])
def send_dead_man():
    policy = Policy.query.filter(Policy.data_id == request.json['data_id']).first()
    query_dict = dict(request.json)
    query_dict["command"] = "delete"
    # the value returned here is a single item list containing the data_id
    SQL_query,SQL_values = craftQuery(query_dict)
    create_pending_policy(policy.policy_id, SQL_query, policy.expiration)
    return make_response(jsonify({'status': 'pending'}))
