from flask import Flask, jsonify
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def index():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hi Guys</h1>
    <p>It is currently {time}.</p>
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

@app.route('/patients')
def patients():
    return """
    <h1>Patient: John Doe</h1>
    <p>Blood Type: A</p>
    """

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
