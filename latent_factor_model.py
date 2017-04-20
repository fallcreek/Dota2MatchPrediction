import pickle
from collections import defaultdict
import json

match = pickle.load(open('./data/match.pkl','rb'))
player = pickle.load(open('./data/players_nonzeor.pkl','rb'))

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
    if hero_id == 0 or player_id == 0:
        exit(0)

    match_id = line['match_id']
    radiant_win = match_dic[match_id]
    is_radiant = (player_slot <= 4)
    if player_id not in player_index:
        player_index[player_id] = index
        index += 1

    if (radiant_win and is_radiant) or (not radiant_win and not is_radiant):
        if player_id not in player_stat:
            player_stat[player_id] = {'win':[0 for _ in range(114)], 'total':[0 for _ in range(114)]}
            player_stat[player_id]['win'][hero_id] = 1
            player_stat[player_id]['total'][hero_id] = 1
        else:
            player_stat[player_id]['win'][hero_id] += 1
            player_stat[player_id]['total'][hero_id] += 1

        if hero_id not in hero_stat:
            hero_stat[hero_id] = {'win':0, 'total':0}
            hero_stat[hero_id]['win'] = 1
            hero_stat[hero_id]['total'] = 1
        else:
            hero_stat[hero_id]['win'] += 1
            hero_stat[hero_id]['total'] += 1
    else:
        if player_id not in player_stat:
            player_stat[player_id] = {'win':[0 for _ in range(114)], 'total':[0 for _ in range(114)]}
            player_stat[player_id]['total'][hero_id] = 1
        else:
            player_stat[player_id]['total'][hero_id] += 1

        if hero_id not in hero_stat:
            hero_stat[hero_id] = {'win':0, 'total':0}
            hero_stat[hero_id]['total'] = 1
        else:
            hero_stat[hero_id]['total'] += 1


# R = [[] for _ in range(len(player_stat))]

f = open('final_data_ratio.json','w')
for player in player_stat:

    # index = player_index[player]
    for i, (w, t) in enumerate(zip(player_stat[player]['win'],player_stat[player]['total'])):
        level = 0
        if t != 0:
            ratio = w * 1.0 / t

            # if ratio < 0.2:
            #     level = 1
            # elif ratio < 0.4:
            #     level = 2
            # elif ratio < 0.6:
            #     level = 3
            # elif ratio < 0.8:
            #     level = 4
            # else:
            #     level = 5
        # R[index].append(level)
            map = {'account_id': player, 'hero_id': i, 'level':ratio}
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


