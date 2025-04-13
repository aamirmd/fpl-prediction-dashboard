from flask import Flask, jsonify, request
from markupsafe import escape
from flask_cors import CORS
from players import name_id_players_map, id_stats_players_map, player_names
from predict import SimpleModel
import torch
app = Flask(__name__)
CORS(app)

#launch flask server with : flask --app backend run
#launch front end with : npm run dev

old_stats = ['xP', 'assists','bonus', 'bps',
'clean_sheets',
 'creativity',
 'goals_conceded',
 'goals_scored',
'ict_index',
'influence',
'minutes',
 'own_goals',
'penalties_missed',
'penalties_saved',
'red_cards',
'saves',
'selected',
'team_a_score',
'team_h_score',
 'threat',
'total_points',
'transfers_in',
 'transfers_out',
 'value',
'was_home',
'yellow_cards']

stats = ['assists', 'bonus', 'bps', 'clean_sheets', 'creativity',
       'goals_conceded', 'goals_scored', 'ict_index', 'influence', 'minutes',
       'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards',
       'saves', 'threat', 'total_points', 'transfers_in', 'transfers_out',
       'yellow_cards']

missing = []
keys = id_stats_players_map[2].keys()
for stat in stats:
    if stat not in keys:
        missing.append(stat)

model = SimpleModel(26)
model.load_state_dict(torch.load('./models/baseline.pth'))
model.eval() 
playerData = []
for i in range(len(stats)):
    if stats[i] in missing:
        playerData.append(0)
    else:
        playerData.append(float(id_stats_players_map[4][stats[i]]))
playerData = torch.tensor(playerData, dtype=torch.float32)
with torch.no_grad():  # Disables gradient calculation for inference
    predictions = model(playerData)

predictions_np = predictions.numpy()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/players", methods=["GET"])
def getPlayers():
    data = player_names
    format = {"data": data}
    json = jsonify(format)
    return json


@app.route("/search/<name>", methods=["GET"])
def search(name):
    clean_name = escape(name)
    id = name_id_players_map[clean_name]
    playerStats = id_stats_players_map[id]
    clean_name = playerStats["first_name"] + " " + playerStats["second_name"] 
    points = predictPoints(id)
    
    data = {"search":clean_name,
            "id": id,
            "points":points
            }
    format = {"data": data}
    json = jsonify(format)
    if request.method == 'GET':
        return json
    else:
        return None

def predictPoints(id):
    playerData = []
    for i in range(len(stats)):
        if stats[i] in missing:
            playerData.append(0)
        else:
            playerData.append(float(id_stats_players_map[id][stats[i]]))
    playerData = torch.tensor(playerData, dtype=torch.float32)
    with torch.no_grad():  # Disables gradient calculation for inference
        predictions = model(playerData)

    predictions_np = str(predictions.numpy()[0])
    return predictions_np