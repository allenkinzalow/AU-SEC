from app import app
from flask import jsonify, request, render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return """
    <h1>Patient: John Doe</h1>
    <p>Blood Type: A</p>
    """