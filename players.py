import requests
import sys
import pandas as pd
import pickle
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
for key, value in retreived_fpl_data.items():
    print(key)

# Creating hashmaps for different data types
positions_map = {pos["id"] : pos["singular_name"] for pos in retreived_fpl_data["element_types"]}
teams_map = {team["id"]: team["name"] for team in retreived_fpl_data["teams"]}
name_id_players_map = {f'{player["first_name"]} {player["second_name"]}': player["id"] for player in retreived_fpl_data["elements"]}
id_stats_players_map = {player["id"] : player for player in retreived_fpl_data["elements"]}

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
fpl_2024_data = pd.read_csv('data/players.csv')
print(fpl_2024_data.head())