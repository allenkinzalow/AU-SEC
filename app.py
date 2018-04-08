from flask import Flask, jsonify, render_template
app = Flask(__name__)

app.config.from_object(__name__)

# Override default configurations in flask.
app.config.update(dict(
    TEMPLATES_AUTO_RELOAD=True
))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

import routes
