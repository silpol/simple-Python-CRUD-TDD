from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return make_response(jsonify({"API":"OK"}),200)

app.run(debug=True)

