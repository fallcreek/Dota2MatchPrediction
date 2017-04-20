import pickle
import numpy as np
import json

# data = pickle.load(open('./data/final_data.pkl','wb'))
# print len(data)

map = {"1":1,"2":2,"3":3,"4":4,"3432":13,"sdfsd":12}
print [i for i in map]

#
# data = open('final_data.json','r')
# for i, line in enumerate(data.readlines()):
#     print  line.strip()
#     if i == 100:
#         break
# f = open('final_data.json','w')
# data = {
#     'account_id': 1,
#     'hero_id': 2,
#     'level': 2
# }
#
#
# json.dump(data,f)
# f.write('\n')
# data = {
#     'account_id': 2,
#     'hero_id': 3,
#     'level': 3
# }
#
# json.dump(data,f)
# f.write('\n')
# train_R = pickle.load(open('./data/R.pkl', 'rb'))
# print 'finish train_R'
#
# user_id = pickle.load(open('./data/player_index.pkl', 'rb'))
# # print user_id
#
# user_map = {}
# item_map = {}
#
# for user in user_id:
#     row = train_R[user_id[user]]
#     map = {}
#     for i in range(len(row)):
#         map[i] = row[i]
#
#     user_map[user] = map
#
# train_R_T = np.matrix(train_R).T
# train_R_T = train_R_T.tolist()
# print len(train_R_T)
# print len(train_R_T[0])
#
# for i,row in enumerate(train_R_T):
#     map = {}
#     for user in user_id:
#         map[user] = train_R_T[i][user_id[user]]
#
#     item_map[i] = map
#
# pickle.dump(user_map, open('user_map.pkl','wb'))
# pickle.dump(item_map, open('item_map.pkl','wb'))
