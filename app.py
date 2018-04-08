
from flask import Flask, jsonify, make_response, request, abort
from datetime import datetime
from database import db_session, init_db
from models import Authorizer_User
import uuid

app = Flask(__name__)
app.config.from_object('config')

app.config.update(dict(
    TEMPLATES_AUTO_RELOAD=True
))

init_db()
u = Authorizer_User(1, 'lmao@gmail.com')
db_session.add(u)
db_session.commit()

app.config.from_object(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

import routes
