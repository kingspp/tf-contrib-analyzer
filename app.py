import json
from flask import Flask, render_template, request, redirect, url_for
import os
import humanize
import datetime


app = Flask(__name__)

usage = json.load(open('./static/data/usage_v1.json'))
stats = json.load(open('./static/data/stats_v1.json'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', total_api=stats['total_api'], total_projects=stats['total_projects'],
                           total_lines = stats['total_lines'], date=humanize.naturaldate(datetime.datetime.fromtimestamp(float(stats['timestamp']))))


@app.route('/get_repos', methods=['GET'])
def get_repos():
    return json.dumps({"data": usage[request.args.get('api', type=str)]})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
