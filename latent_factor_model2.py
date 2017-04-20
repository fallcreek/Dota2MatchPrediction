import pickle
import json
import gzip

f = open('final_data_kda.json','r')

user_id = {}
item_id = {}

user_number = -1


train_data = []
for l in f.readlines():
    l = json.loads(l)
    train_data.append(l)
    user, item = l['account_id'],l['hero_id']
    if user not in user_id:
        user_number += 1
        user_id[user] = user_number


print('finish reading id')
item_number = 113


train_R = pickle.load(open('train_R.pkl', 'rb'))
print 'finish train_R'



def converge(alpha, pre_alpha, iteration, threshold):
    if iteration == 1:
        return False

    if abs(alpha - pre_alpha) > threshold:
        return False

    return True

def MSE(alpha, bu, bi):
    mse = 0
    for l in train_data:
        user, item = l['account_id'], l['hero_id']
        predict_level = alpha + bu[user_id[user]] + bi[item]
        # print predict_level
        level = l['level']
        mse += (predict_level - level) ** 2;

    return mse/len(train_data)


def model1():
    threshold = 0.0000000000001
    lam_list = range(6484690, 6484710, 1)
    lam_list = [5.61]
    mse_list = []

    for lam in lam_list:
        # lam = lam * 1.0 / 1000000
        print('lam = ' + str(lam))

        # init
        alpha = 0.0
        bu = [0.0 for i in range(user_number + 1)]
        bi = [0.0 for i in range(item_number + 1)]
        iteration = 1

        pre_alpha = alpha
        pre_mse = 20

        while not converge(alpha, pre_alpha, iteration, threshold):
            pre_alpha = alpha

            iteration += 1
            print 'this is the ' + str(iteration) + ' iteration'
            sum_alpha = 0.0
            for line in train_data:
                user = int(line['account_id'])
                hero_id = int(line['hero_id'])
                if hero_id == 0 or user == 0:
                    print line
                    exit(1)

                R_u_i = train_R[user_id[user]][hero_id]
                b_u = bu[user_id[user]]
                b_i = bi[hero_id]
                sum_alpha += R_u_i - (b_u + b_i)
            alpha = sum_alpha / len(train_data)
            print(alpha)

            temp_b_u = [0.0 for i in bu]
            I_u = [0.0 for i in bu]
            for line in train_data:
                user = int(line['account_id'])
                hero_id = int(line['hero_id'])
                if hero_id == 0 or user == 0:
                    exit(1)
                R_u_i = train_R[user_id[user]][hero_id]
                temp_b_u[user_id[user]] += R_u_i - (alpha + bi[hero_id])
                I_u[user_id[user]] += 1

            for i in range(len(bu)):
                bu[i] = temp_b_u[i] / (lam + I_u[i])


            temp_b_i = [0.0 for i in bi]
            U_i = [0.0 for i in bi]
            for line in train_data:
                user = int(line['account_id'])
                hero_id = int(line['hero_id'])
                if hero_id == 0 or user == 0:
                    exit(1)
                R_u_i = train_R[user_id[user]][hero_id]
                temp_b_i[hero_id] += R_u_i - (alpha + bu[user_id[user]])
                U_i[hero_id] += 1

            for i in range(len(bi)):
                bi[i] = temp_b_i[i] / (lam + U_i[i])


            mse = MSE(alpha, bu, bi)
            if pre_mse - mse < 0.00000000001:
                break
            pre_mse = mse
            print('MSE = ' + str(mse))
            mse_list.append(mse)



    # min_mse = min(mse_list)
    # min_index = mse_list.index(min_mse)
    # print('The optimal lambda is ' + str(lam_list[min_index]))
    return alpha, bu, bi

alpha, bu, bi = model1()



# X = []
# Y = []
#
# index = -1
# match = []
# for l in data:
#     match_id = int(l['match_id'])
#     if match_id not in match:
#         index += 1
#         Y.append(match_dic[match_id])
#         X.append([])
#
#     X[len(X) - 1].append(int(l['account_id']))
#     X[len(X) - 1].append(int(l['hero_id']))
#
# def cal(user, hero):
#
#
# for x, y in zip(X, Y):


def cal(user, hero):
    if hero == 0:
        return alpha

    if user not in user_id:
        return alpha + 2 * bi[hero]
    else:
        return alpha + bu[user_id[user]] + bi[hero]


test_labels = pickle.load(open('test_labels.pkl','rb'))
test_account = pickle.load(open('test_account.pkl','rb'))
test_hero = pickle.load(open('test_hero.pkl','rb'))
print 'finishing reading test'

total = 0
corr = 0

for match in test_labels:
    print 'match = ' + str(match['match_id'])
    match_id = match['match_id']
    team1 = sum([cal(int(user), int(hero)) for user, hero in zip(test_account[match_id][0:5], test_hero[match_id][0:5])])
    team2 = sum([cal(int(user), int(hero)) for user, hero in zip(test_account[match_id][5:], test_hero[match_id][5:])])

    if team1 > team2:
        predict = 1
        print 'predict win'
    else:
        predict = 0
        print 'predict lose'


    if predict == int(match['radiant_win']):
        print 'correct'
        corr += 1

    total += 1

print corr * 1.0 / total

