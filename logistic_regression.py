import numpy
import urllib
import scipy.optimize
import random
from math import exp
from math import log
import  pickle
import gzip
from collections import defaultdict
import numpy as np
import scipy.optimize
from math import exp, log
from math import floor, ceil
import csv
import json
import gzip
import pickle
import gzip
import numpy as np
from collections import defaultdict
import urllib
import scipy.optimize
import random
from collections import defaultdict
from sklearn import linear_model
from math import sqrt

coop_map = pickle.load(open('hero_combine.pkl','rb'))
counter_map = pickle.load(open('hero_counter.pkl','rb'))


label = pickle.load(open('./data/match_win.pkl','rb'))

match_win = {}
for match_id in label:
    if label[match_id] == "True":
        match_win[match_id] = 1
    else:
        match_win[match_id] = 0

# print match_win

# train_account = pickle.load(open('train_account.pkl','rb'))
train_hero = pickle.load(open('train_hero.pkl','rb'))
hero_type = pickle.load(open('hero_type.pkl','rb'))
type_feat_map = pickle.load(open('type_feat.pkl','rb')) # (r,g,b) -> index in type_feat
hero_winrate = pickle.load(open('hero_win_appear.pkl','rb'))

def feature(match_id,train_hero):
    feat = [1]

    # win_rate = 0.0
    # for i in range(0, 5):
    #     hero1 = int(train_hero[match_id][i])
    #     if hero1 == 0:
    #         continue
    #     win_rate += hero_winrate[hero1][0]
    #
    # feat.append(win_rate/5)
    #
    # win_rate = 0.0
    # for i in range(0, 5):
    #     hero1 = int(train_hero[match_id][i])
    #     if hero1 == 0:
    #         continue
    #     win_rate += hero_winrate[hero1][0]
    #
    # feat.append(win_rate / 5)

    # type_feat_1 = [0,0,0]
    #
    # for i in range(0, 5):
    #     hero1 = int(train_hero[match_id][i])
    #     if hero1 == 0:
    #         continue
    #
    #     type1 = hero_type[hero1]
    #     if type1 == 'g':
    #         type_feat_1[1] = 1
    #     elif type1 == 'r':
    #         type_feat_1[0] = 1
    #     elif type1 == 'b':
    #         type_feat_1[2] = 1
    #     else:
    #         exit(1)
    #
    # for f in type_feat_1:
    #     feat.append(f)
    #
    #
    # type_feat_2 = [0,0,0]
    #
    # for i in range(5, 10):
    #     hero2 = int(train_hero[match_id][i])
    #     if hero2 == 0:
    #         continue
    #
    #     type2 = hero_type[hero2]
    #     if type2 == 'g':
    #         type_feat_2[1] = 1
    #     elif type2 == 'r':
    #         type_feat_2[0] = 1
    #     elif type2 == 'b':
    #         type_feat_2[2] = 1
    #     else:
    #         exit(1)
    #
    # for f in type_feat_2:
    #     feat.append(f)


    # team1_hero = [0 for _ in range(113)]
    # team2_hero = [0 for _ in range(113)]
    #
    # for hero_id in train_hero[match_id][0:5]:
    #     team1_hero[int(hero_id)] = 1
    #
    # for hero_id in train_hero[match_id][5:10]:
    #     team2_hero[int(hero_id)] = 1
    #
    # for f in team1_hero:
    #     feat.append(f)
    #
    # for f in team2_hero:
    #     feat.append(f)

    team1_coop = 0.0
    for i in range(0,5):
        for j in range(i+1,5):
            hero1 = int(train_hero[match_id][i])
            hero2 = int(train_hero[match_id][j])

            first = min(hero1, hero2)
            second = max(hero1, hero2)
            if first == 0:
                # team1_coop -= 0.1
                continue
            team1_coop += coop_map[first][second]

    team2_coop = 0.0
    for i in range(5, 10):
        for j in range(i + 1, 10):
            hero1 = int(train_hero[match_id][i])
            hero2 = int(train_hero[match_id][j])

            first = min(hero1, hero2)
            second = max(hero1, hero2)
            if first == 0:
                # team1_coop += 0
                continue
            team2_coop += coop_map[first][second]

    diff_coop = team1_coop/10 - team2_coop/10
    # print diff_coop
    feat.append(diff_coop)

    counter = 0.0
    for i in range(0, 5):
        for j in range(5, 10):
            hero1 = int(train_hero[match_id][i])
            hero2 = int(train_hero[match_id][j])
            if hero1 == 0 or hero2 == 0:
                continue

            counter += counter_map[hero1][hero2]

    feat.append(counter/25)
    return feat

def inner(x,y):
  return sum([x[i]*y[i] for i in range(len(x))])

def sigmoid(x):
  return 1.0 / (1 + exp(-x))

def f(theta, X, y, lam):
  # print(theta)
  loglikelihood = 0
  for i in range(len(X)):
    logit = inner(X[i], theta)
    loglikelihood -= log(1 + exp(-logit))
    if not y[i]:
      loglikelihood -= logit
  for k in range(len(theta)):
    loglikelihood -= lam * theta[k]*theta[k]
  print("ll =", loglikelihood)
  return -loglikelihood

# NEGATIVE Derivative of log-likelihood
def fprime(theta, X, y, lam):
  dl = [0.0]*len(theta)
  for k in xrange(len(theta)):
    print k
    for i in xrange(len(X)):
      # Fill in code for the derivative
      dl[k] += (X[i][k] * (1 - sigmoid(numpy.inner(X[i], theta))))
      if not y[i]:
        dl[k] -= X[i][k]
    dl[k] -= lam * 2 * theta[k]
  print(dl)
  # Negate the return value since we're doing gradient *ascent*
  return numpy.array([-x for x in dl])

X_train = [feature(match_id,train_hero) for match_id in match_win]
y_train = [match_win[match_id] for match_id in match_win]

print X_train[0]
print sum(y_train) * 1.0/len(y_train)

theta,l,info = scipy.optimize.fmin_l_bfgs_b(f, [0]*len(X_train[0]), fprime, args = (X_train, y_train, 1))
print theta


def accuracy(theta, X, Y):
    count = 0
    for x, y in zip(X, Y):
        res = inner(theta, x)
        if res > 0 and y == 1 or res <= 0 and y == 0:
            count += 1

    return count * 1.0 / len(Y)

print accuracy(theta,X_train,y_train)




test_labels = pickle.load(open('test_labels.pkl','rb'))
# test_account = pickle.load(open('test_account.pkl','rb'))
test_hero = pickle.load(open('test_hero.pkl','rb'))


X_test = [feature(str(match['match_id']), test_hero) for match in test_labels]
y_test = [int(match['radiant_win']) for match in test_labels]




print accuracy(theta,X_test,y_test)

