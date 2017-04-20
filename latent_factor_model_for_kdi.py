import pickle
from collections import defaultdict
import json

match = pickle.load(open('./data/match.pkl','rb'))
player = pickle.load(open('./data/players.pkl','rb'))

# player = [ l for l in player if l['account_id'] != '0' and l['hero_id'] != '0']
# pickle.dump(player, open('./players_nonzeor.pkl','wb'))
# exit(0)

print len(player)
print len(match)
print 'read done'

match_dic = pickle.load(open('./data/match_win.pkl','rb'))
# print (match_dic[0] == True)

player_stat = {}
hero_stat = {}

player_index = {}
index = 0
print len(player)


for i, line in enumerate(player):
    # print i
    player_slot = int(line['player_slot'])
    player_id = int(line['account_id'])
    hero_id = int(line['hero_id'])
    if hero_id == 0:
        continue

    match_id = line['match_id']
    radiant_win = match_dic[match_id]
    is_radiant = (player_slot <= 4)
    if player_id not in player_index:
        player_index[player_id] = index
        index += 1

    if player_id not in player_stat:
        player_stat[player_id] = {'kda': [0 for _ in range(114)],'number' : [0 for _ in range(114)]}

    ratio = (int(line['kills']) + int(line['assists'])) * 1.0 / (int(line['deaths']) + 1 )
    player_stat[player_id]['kda'][hero_id] += ratio
    player_stat[player_id]['number'][hero_id] += 1


# R = [[] for _ in range(len(player_stat))]

f = open('final_data_kda.json','w')
for player in player_stat:

    # index = player_index[player]
    for i, (k, n) in enumerate(zip(player_stat[player]['kda'],player_stat[player]['number'])):
        if n > 0:
            ave = k * 1.0 / n
            map = {'account_id': player, 'hero_id': i, 'kda': ave}
            json.dump(map, f)
            f.write('\n')


# print final_data
# pickle.dump(final_data, open('./data/final_data.pkl','wb'))


# pickle.dump(R, open('./data/R.pkl', 'wb'))

# print len([player_stat[i] for i in player_stat if player_stat[i]['total'] > 2])
# # print hero_stat
# print (hero_stat)
#
# pickle.dump(hero_stat, open('./data/hero_stat.pkl', 'wb'))
# pickle.dump(player_index, open('./data/player_index.pkl','wb'))


