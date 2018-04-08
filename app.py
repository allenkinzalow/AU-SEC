
from flask import Flask, jsonify, make_response, request, abort
from datetime import datetime
from database import db_session, init_db
from models import Authorizer_User
import uuid
from routes import routes

app = Flask(__name__)
app.config.from_object('config')

init_db()

app.register_blueprint(routes)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	if 'message' in error.description:
		response = jsonify({'error': 400, 'message': error.description['message'], 'status': 'error'})
	else:
		response = jsonify({'error': 400, 'message': 'Bad request sent to the server'})
	return make_response(response, 400)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


