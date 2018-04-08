
from flask import Flask, jsonify, make_response, request, abort
from datetime import datetime
from database import db_session, init_db
from models import Authorizer_User
import uuid
from dispatch.Dispatcher import Dispatcher

app = Flask(__name__)
app.config.from_object('config')

init_db()

def check_json(json, *params):
    if not json:
        return False
    for key in params:
        if not key in json:
            return False
    return True

@app.route('/')
def index():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hi Guys</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=app.config["MYSQL_USER"])


# {preferred_comms: <integer>{1,2,3}, contact_info: <string>}
@app.route('/api/auth_users/create_user', methods=['POST'])
def create_user():
    if not check_json(request.json, 'preferred_comms', 'contact_info'):
        abort(400)
    user = Authorizer_User(request.json['preferred_comms'], request.json['contact_info'])
    db_session.add(user)
    db_session.commit()
    return make_response(jsonify({"id": user.auth_id}), 200)

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

# {row_id: id, new_data: {column_name: column, ...}}
@app.route('/api/data/update', methods=['PUT'])
def update_data():    
    return

# {data: {table_name: "", column_name: "", }}
@app.route('/api/data/select', methods=['PUT'])
def select_data():    
    return

# {data: {column_names: column_data}, table_name: table, authorized_user: id}
@app.route('/api/data/insert', methods=['POST'])
def insert_data():
    if not check_json(request.json, 'authorized_user', 'data'):
        abort(400)

    return

# {row_id: id, table_name: table}
@app.route('/api/data/delete', methods=['PUT'])
def delete_data():
    if not check_json(request.json, 'row_id'):
        abort(400)
    return

@app.route('/api/data/view_history', methods=[''])
def view_data_history():    
    return

@app.route('/api/dispatch/send')
def send_auth_reqiest():
    return

@app.route('/api/dispatch/receive')
def get_auth_update():
    return

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/patients')
def patients():
    return """
    <h1>Patient: John Doe</h1>
    <p>Blood Type: A</p>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

