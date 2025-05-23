from flask import Flask, jsonify, request
from markupsafe import escape
from flask_cors import CORS
from predict import SimpleModel
import torch
import pulp as p
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
       'saves', 'threat', 'total_points', 'transfers_in_event', 'transfers_out_event',
       'yellow_cards']

""" ['assists', 'bonus', 'bps', 'clean_sheets', 'creativity',
       'goals_conceded', 'goals_scored', 'ict_index', 'influence', 'minutes',
       'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards',
       'saves', 'threat', 'total_points', 'transfers_in', 'transfers_out',
       'yellow_cards', 'is_home'] """
model = SimpleModel(21)
model.load_state_dict(torch.load('./models/residual-2.pth'))
model.eval() 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/players", methods=["GET"])
def getPlayers():
    from players import player_basics

    data = player_basics
    format = {"data": data}
    json = jsonify(format)
    return json


@app.route("/search/<name>", methods=["GET"])
def search(name):
    from players import name_id_players_map, id_stats_players_map
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
    
@app.route("/transfer", methods=["POST"])
def transferRec():
    data = request.get_json()
    
    recommendation = getRec(data['selectedPlayers'], data['bank'])
    format = {"data": recommendation}
    json = jsonify(format)
    return json

def getRec(players, bank):
    from players import player_basics
    recommendedTransfer = {}
    bank = float(bank)
    for playerOut in players:
    # choose 3 , no repeats, so remove candidate from pool
        candidates = [player for player in player_basics if player not in players and player['position'] == playerOut['position']]
        playerOutTeam = playerOut['team']
        availableBank = bank + float(playerOut['cost'])

        # remove this player from team count
        playerTeams = {}
        for player in players:
            team = player['team']
            if team not in playerTeams:
                playerTeams[team] = 1
            else:
                playerTeams[team] += 1

        playerTeams[playerOutTeam] -= 1
        # get all possible candidates, make optimal selection later
        for candidate in candidates:
            candidateID = candidate['id']
            # check team constraint
            candTeam = candidate['team']
            if candTeam in playerTeams and playerTeams[candTeam] == 3:
                continue
            # check balance constraint
            if float(candidate['cost']) > availableBank:
                continue
            # we only want players that are doing better
            if float(candidate['predictedPoints']) <= float(playerOut['predictedPoints']):
                continue
            # we reached a candidate
            # add to rec list, check if player in already in there, calcualte delta pred points and choose the higher one
            delta = float(candidate['predictedPoints']) - float(playerOut['predictedPoints'])
            delta = delta/float(playerOut['predictedPoints'])
            if candidateID not in recommendedTransfer:
                recommendedTransfer[candidateID] = {"playerIn":candidate, "playerOut": playerOut, "delta":delta}
            else:
                # candidate already in list, check for higher delta
                currDelta = float(recommendedTransfer[candidateID]["delta"])
                if delta > currDelta:
                    recommendedTransfer[candidateID] = {"playerIn":candidate,"playerOut": playerOut, "delta":delta}

    # sort by delta
    sortedRecs = dict(sorted(recommendedTransfer.items(), key=lambda x: x[1]['delta'], reverse=True)[:3])
    sortedRecs = list(sortedRecs.values())
    return sortedRecs

def predictPoints(id):
    from players import gwStats_map, id_stats_players_map, id_ishome_nextgame
    # use global stats list
    playerData = []
    if (id in gwStats_map):
        playerGWStats = gwStats_map[int(id)]
        for i in range(len(stats)):
            if stats[i] in playerGWStats:
                playerData.append(float(playerGWStats[stats[i]]))
            else:
                playerData.append(float(id_stats_players_map[id][stats[i]]))
        # add is home as last element in the list
        if id_stats_players_map[id]['team'] in id_ishome_nextgame:
            playerData.append(float(id_stats_players_map[id]['team']))
        else:
            playerData.append(float(-1))
        playerData = torch.tensor(playerData, dtype=torch.float32)
        with torch.no_grad():  # Disables gradient calculation for inference
            predictions = model(playerData)
        predictions_np = str(predictions.numpy()[0])
        return predictions_np
    else:
        return -1