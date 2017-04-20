import pickle
import json
import gzip
import numpy as np

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


train_R = pickle.load(open('train_R_kda.pkl', 'rb'))
print 'finish train_R_kda'



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
        level = l['kda']
        mse += (predict_level - level) ** 2;

    return mse/len(train_data)

def MSE_2(alpha, bu, bi, ru, ri):
    mse = 0
    for l in train_data:
        user, item = l['account_id'], l['hero_id']
        predict = alpha + bu[user_id[user]] + bi[item] + inner(ru[user_id[user]],ri[item])
        mse += (l['kda'] - predict) ** 2

    return (mse / len(train_data))

def model1():
    threshold = 0.0000000000001
    lam_list = range(1, 10, 1)
    lam_list = [2]
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
                if hero_id == 0:
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
                if hero_id == 0:
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
                if hero_id == 0:
                    exit(1)
                R_u_i = train_R[user_id[user]][hero_id]
                temp_b_i[hero_id] += R_u_i - (alpha + bu[user_id[user]])
                U_i[hero_id] += 1

            for i in range(len(bi)):
                bi[i] = temp_b_i[i] / (lam + U_i[i])


            mse = MSE(alpha, bu, bi)
            print('MSE = ' + str(mse))
            if pre_mse - mse < 0.00000000001:
                mse_list.append(mse)
                break
            pre_mse = mse

    print mse_list
    min_mse = min(mse_list)
    print min_mse
    min_index = mse_list.index(min_mse)
    print min_index
    print('The optimal lambda is ' + str(lam_list[min_index]))
    return alpha, bu, bi

alpha, bu, bi = model1()

k = 6
ru = np.random.rand(user_number+1,k)
ri = np.random.rand(item_number+1,k)

def inner(x,y):
  return sum([x[i]*y[i] for i in range(len(x))])

def model2(k, ru, ri):
    threshold = 0.00000000000000001
    lam_list = range(6484690, 6484710, 1)
    lam_list = [2]
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
            print('iteration' + str(iteration))
            temp_r_i_k = [[0.0 for i in range(0, k)] for j in bi]
            for components in range(0, k):
                temp_i = [0.0 for j in bi]
                rik_sum = 0.0
                for line in train_data:
                    user = int(line['account_id'])
                    hero_id = int(line['hero_id'])
                    R_u_i = train_R[user_id[user]][hero_id]
                    temp_i[hero_id] += ru[user_id[user]][components] * (R_u_i - (
                    alpha + bu[user_id[user]] + bi[hero_id] + inner(ru[user_id[user]], ri[hero_id]) - ru[user_id[user]][components] * ri[hero_id][components]))
                    rik_sum += ri[hero_id][components]**2
                for index, item in enumerate(temp_i):
                    temp_r_i_k[index][components] = item / (lam + rik_sum)
                # print(temp_r_i_k[item_id[item]][components])
            ri = temp_r_i_k
            # print(ri)

            temp_r_u_k = [[0.0 for i in range(0, k)] for j in bu]
            for components in range(0, k):
                temp_u = [0.0 for u in bu]
                ruk_sum = 0.0
                for line in train_data:
                    user = int(line['account_id'])
                    hero_id = int(line['hero_id'])
                    R_u_i = train_R[user_id[user]][hero_id]
                    temp_u[user_id[user]] += ri[hero_id][components] * (R_u_i - (
                        alpha + bu[user_id[user]] + bi[hero_id] + inner(ru[user_id[user]], ri[hero_id]) - ru[user_id[user]][components] * ri[hero_id][components]))
                    ruk_sum += ru[user_id[user]][components]**2
                for index, user in enumerate(temp_u):
                    temp_r_u_k[index][components] = user / (lam + ruk_sum)
            ru = temp_r_u_k
            # print(ru)


            sum_alpha = 0.0
            for line in train_data:
                user = int(line['account_id'])
                hero_id = int(line['hero_id'])
                R_u_i = train_R[user_id[user]][hero_id]
                b_u = bu[user_id[user]]
                b_i = bi[hero_id]
                sum_alpha += R_u_i - (b_u + b_i + inner(ru[user_id[user]],ri[hero_id]))
            alpha = sum_alpha / len(train_data)
            print(alpha)

            temp_b_u = [0.0 for i in bu]
            I_u = [0.0 for i in bu]
            for line in train_data:
                user = int(line['account_id'])
                hero_id = int(line['hero_id'])
                R_u_i = train_R[user_id[user]][hero_id]
                temp_b_u[user_id[user]] += R_u_i - (alpha + bi[hero_id] + inner(ru[user_id[user]],ri[hero_id]))
                I_u[user_id[user]] += 1

            for i in range(len(bu)):
                bu[i] = temp_b_u[i] / (lam + I_u[i])

            temp_b_i = [0.0 for i in bi]
            U_i = [0.0 for i in bi]
            for line in train_data:
                user = int(line['account_id'])
                hero_id = int(line['hero_id'])
                R_u_i = train_R[user_id[user]][hero_id]
                temp_b_i[hero_id] += R_u_i - (alpha + bu[user_id[user]] + inner(ru[user_id[user]],ri[hero_id]))
                U_i[hero_id] += 1

            for i in range(len(bi)):
                bi[i] = temp_b_i[i] / (lam + U_i[i])

            mse = MSE_2(alpha, bu, bi, ru, ri)
            print('MSE = ' + str(mse))
            if pre_mse - mse < 0.00000000001:
                mse_list.append(mse)
                break
            pre_mse = mse



    # min_mse = min(mse_list)
    # min_index = mse_list.index(min_mse)
    # print('The optimal lambda is ' + str(lam_list[min_index]))
    return alpha, bu, bi, ru, ri

# alpha, bu, bi, ru, ri = model2(k, ru, ri)


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

def cal_2(user, hero):
    if hero == 0:
        return alpha

    if user not in user_id:
        return alpha + 2 * bi[hero]
    else:
        return alpha + bu[user_id[user]] + bi[hero] + inner(ru[user_id[user]],ri[hero])

test_labels = pickle.load(open('test_labels.pkl','rb'))
test_account = pickle.load(open('test_account.pkl','rb'))
test_hero = pickle.load(open('test_hero.pkl','rb'))
print 'finishing reading test'

total = 0
corr = 0

for match in test_labels[:5000]:
    # print 'match = ' + str(match['match_id'])
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

