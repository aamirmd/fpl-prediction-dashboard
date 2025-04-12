import requests
import sys
import pandas as pd
import pickle
from predict import SimpleModel
import torch
#import kagglehub
sys.stdout.reconfigure(encoding='utf-8') # needs utf-8 for fetched data


# Download latest version
""" path = kagglehub.dataset_download("meraxes10/fantasy-premier-league-2024")

print("Path to dataset files:", path) """


def fpl_api():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
    except:
        return None

retreived_fpl_data = fpl_api()   
""" for key, value in retreived_fpl_data.items():
    print(key) """

# Creating hashmaps for different data types
positions_map = {pos["id"] : pos["singular_name"] for pos in retreived_fpl_data["element_types"]}
teams_map = {team["id"]: team["name"] for team in retreived_fpl_data["teams"]}
#lowered all the names
name_id_players_map = {f'{player["first_name"]} {player["second_name"]}'.lower(): player["id"] for player in retreived_fpl_data["elements"]}
id_stats_players_map = {player["id"] : player for player in retreived_fpl_data["elements"]}
player_basics = []#{'name':f'{player["first_name"]} {player["second_name"]}', f'' for player in retreived_fpl_data["elements"]}
for player in retreived_fpl_data["elements"]:
    if (positions_map[player['element_type']] != 'Manager'):
        basicInfo = {"name": f'{player["first_name"]} {player["second_name"]}',
                    "id":player["id"],
                    "position": f'{positions_map[player['element_type']]}',
                    "team":f'{teams_map[player["team"]]}',
                    "cost": f'{player['now_cost']}'}
        player_basics.append(basicInfo)
#print(f'players: {player_names}')
#print(len(player_names))
# Storing hashmaps as pickle files
with open('data/positions_map.pkl', 'wb') as f:
    pickle.dump(positions_map, f)

with open('data/teams_map.pkl', 'wb') as f:
    pickle.dump(teams_map, f)

with open('data/name_id_players_map.pkl', 'wb') as f:
    pickle.dump(name_id_players_map, f)

with open('data/id_stats_player_map.pkl', 'wb') as f:
    pickle.dump(id_stats_players_map, f)


#print(positions_map)
##fpl_2024_data = pd.read_csv('data/players.csv')
#print(fpl_2024_data.head())
stats = ['xP', 'assists','bonus', 'bps',
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
print("[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]")
missing = []
keys = id_stats_players_map[2].keys()
for stat in stats:
    if stat not in keys:
        missing.append(stat)
 
""" model = SimpleModel(26)
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
print("Predictions for test dataset:")
print(predictions_np) """
#####print(id_stats_players_map[2])
 
