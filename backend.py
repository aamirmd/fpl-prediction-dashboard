from flask import Flask, jsonify, request
from markupsafe import escape
from flask_cors import CORS
from players import name_id_players_map, id_stats_players_map
app = Flask(__name__)
CORS(app)

#launch flask server with : flask --app backend run
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/search/<name>", methods=["GET"])
def search(name):
    clean_name = escape(name)
    id = name_id_players_map[clean_name]
    goals = id_stats_players_map[id]["goals_scored"]
    data = {"search":clean_name,
            "id": id,
            "goals":goals
            }
    format = {"data": data}
    json = jsonify(format)
    if request.method == 'GET':
        return json
    else:
        return None