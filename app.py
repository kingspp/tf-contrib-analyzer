import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

usage = json.load(open('./static/data/usage.json'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get_repos', methods=['GET'])
def get_repos():
    return json.dumps({"data": usage[request.args.get('api', type=str)]})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
