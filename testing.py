from players import  player_basics, name_id_players_map, id_stats_players_map
import random

# for each player in team, simulate them being swapped out, get 3 highest pred points for each of them, then sort, then get highest three

# CONSTRAINTS:
# same position : fwd for fwd, def for def, etc
# no more than 3 players from same team : CHECK WITH playerteams dict
# cost : player rec cost <= bank + player out
 
testTeam = []
# format : player in : player out
recs = {}
candidates = {}
for i in range(13):
    index = random.randint(0, len(player_basics))
    testTeam.append(player_basics[index])

test1 = name_id_players_map['Mohamed Salah'.lower()]
test2 = name_id_players_map['Alexander Isak'.lower()]
test3 = name_id_players_map['Omar Marmoush'.lower()]

for p in player_basics:
    if p['id'] == test1 or p['id'] == test2 or p['id'] == test3:
        testTeam.append(p)
 
bank = 50

# for each player in selected team

for playerOut in testTeam:
    
    # choose 3 , no repeats, so remove candidate from pool
    candidates = [player for player in player_basics if player not in testTeam and player['position'] == playerOut['position']]
    playerOutTeam = playerOut['team']
    availableBank = bank + float(playerOut['cost'])

    # remove this player from team count
    playerTeams = {}
    for player in testTeam:
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
        if candidateID not in recs:
            recs[candidateID] = {"playerIn":candidate, "playerOut": playerOut, "delta":delta}
        else:
            # candidate already in list, check for higher delta
            currDelta = float(recs[candidateID]["delta"])
            if delta > currDelta:
                recs[candidateID] = {"playerIn":candidate,"playerOut": playerOut, "delta":delta}

# sort by delta
sortedRecs = dict(sorted(recs.items(), key=lambda x: x[1]['delta'], reverse=True)[:3])
print(sortedRecs)
#print(list(sorted(recs.items(), key=lambda x: x[1]['delta'], reverse=True))[:7])
 






