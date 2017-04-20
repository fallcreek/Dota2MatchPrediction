import pickle
import json
f = open('final_data_kda.json','r')

user_id = {}
item_id = {}

user_number = -1

for l in f.readlines():
    l = json.loads(l)
    user, item = l['account_id'],l['hero_id']
    if user not in user_id:
        user_number += 1
        user_id[user] = user_number

print('finish reading id')

item_number = 113

train_R = [[0 for i in range(item_number + 1)] for j in range(user_number + 1)]
print('finish init train_R')

f = open('final_data_kda.json','r')
for l in f.readlines():
    l = json.loads(l)
    user, item = l['account_id'], l['hero_id']
    rating = l['kda']
    user_index = user_id[user]
    item_index = item
    train_R[user_index][item_index] = rating

g = open('train_R_kda.pkl','wb')
pickle.dump(train_R, g)