from flask import Flask, render_template, send_from_directory, jsonify
from pydblite.pydblite import Base
from collections import Counter

app = Flask(__name__)

def store():
    db = Base('analytics.pydb', save_to_file=True)
    if db.exists():
        db.open()
    else:
        db.create('user_id', 'action', 'vedio_id', 'viewed_time', 'total_time', 'seeked')
    return db

db = store()

@app.route('/js/<file>')
def send_js(file):
    return send_from_directory('/Users/gunapati/projects/snowplow-javascript-tracker/dist', file)

@app.route("/schemas/com.tectoro/viewed-vedio/jsonschema/1-0-0")
def local_iglu():
    return send_from_directory('/Users/gunapati/projects/snowplowDesign/templates', "viewed_vedio.json")

@app.route('/favicon.ico')
def favicon():
    return ""

@app.route("/<usr>")
def home(usr):
    return render_template("vedios.html", user=usr)

@app.route("/analytics")
def load():
    db = Base('analytics.pydb').open()
    return jsonify({
        "most_watched_vedio_cnt": dict(Counter([r['vedio_id'] for r in (db('action')=='started')])),
        "most_watched_user_cnt": dict(Counter([r['user_id'] for r in db])),
        "most_seeked_vedio_cnt": dict(Counter([r['vedio_id'] for r in (db('seeked')=='true')])),
    })


if __name__ == '__main__':
    app.run(debug=True)