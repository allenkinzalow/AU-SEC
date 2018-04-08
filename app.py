from flask import Flask, jsonify, render_template
from datetime import datetime
app = Flask(__name__)

# Override default configurations in flask.
app.config.update(dict(
    TEMPLATES_AUTO_RELOAD=True
))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return """
    <h1>Patient: John Doe</h1>
    <p>Blood Type: A</p>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
