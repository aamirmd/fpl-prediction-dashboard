import requests
import sys
sys.stdout.reconfigure(encoding='utf-8') # needs utf-8 for fetched data

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
name_id_players_map = {f'{player["first_name"]} {player["second_name"]}': player["id"] for player in retreived_fpl_data["elements"]}
id_stats_players_map = {player["id"] : player for player in retreived_fpl_data["elements"]}
print(id_stats_players_map)