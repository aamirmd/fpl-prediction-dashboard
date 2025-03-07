import requests
import sys
import pandas as pd
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
positions_map = {pos["id"] : pos["singular_name"] for pos in retreived_fpl_data["element_types"]}
teams_map = {team["id"]: team["name"] for team in retreived_fpl_data["teams"]}
#lowered all the names
name_id_players_map = {f'{player["first_name"]} {player["second_name"]}'.lower(): player["id"] for player in retreived_fpl_data["elements"]}
id_stats_players_map = {player["id"] : player for player in retreived_fpl_data["elements"]}
# print(positions_map)
#fpl_2024_data = pd.read_csv('players.csv')
#print(fpl_2024_data.head())
print(id_stats_players_map)
