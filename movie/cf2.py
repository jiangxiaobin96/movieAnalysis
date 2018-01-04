# coding: utf-8
import sys
import numpy as np
import pandas as pd
from numpy import linalg as la
import csv


username = list(range(313))
data = {}
f = open("user.txt")
line = f.readline()
i=0
while line:
    username[i] = line.rstrip("\n")
    line = f.readline()
    i=i+1
f.close()
print(username)
f = open("result.txt",encoding='UTF-8')
line = f.readline()
while line:
    a = line.split("\t")
    # print(a[0],a[1],a[2])
    # print(type(a[2]))
    if a[0] not in data:
        data[a[0]] = {}
        data[a[0]][a[1]] = int(a[2])
    else:
        if a[1] not in data[a[0]]:
            data[a[0]][a[1]] = int(a[2])
        else:
            data[a[0]][a[1]].append(int(a[2]))
    line = f.readline()
f.close()
print(data)


# clean&transform the data
data = pd.DataFrame(data)
# 0 represents not been rated
data = data.fillna(0)
# each column represents a movie
mdata = data.T

# calculate the simularity of different movies, normalize the data into [0,1]
np.set_printoptions(3)
mcors = np.corrcoef(mdata, rowvar=0)
mcors = 0.5 + mcors * 0.5
mcors = pd.DataFrame(mcors, columns=mdata.columns, index=mdata.columns)


# calculate the score of every item of every user
# matrix:the user-movie matrix
# mcors:the movie-movie correlation matrix
# item:the movie id
# user:the user id
# score:score of movie for the specific user
def cal_score(matrix, mcors, item, user):
    totscore = 0
    totsims = 0
    score = 0
    if pd.isnull(matrix[item][user]) or matrix[item][user] == 0:
        for mitem in matrix.columns:
            if matrix[mitem][user] == 0:
                continue
            else:
                totscore += matrix[mitem][user] * mcors[item][mitem]
                totsims += mcors[item][mitem]
        score = totscore / totsims
    else:
        score = matrix[item][user]
    return score


# calculate the socre matrix
# matrix:the user-movie matrix
# mcors:the movie-movie correlation matrix
# score_matrix:score matrix of movie for different users
def cal_matscore(matrix, mcors):
    score_matrix = np.zeros(matrix.shape)
    score_matrix = pd.DataFrame(score_matrix, columns=matrix.columns, index=matrix.index)
    for mitem in score_matrix.columns:
        for muser in score_matrix.index:
            score_matrix[mitem][muser] = cal_score(matrix, mcors, mitem, muser)
    return score_matrix


# give recommendations: depending on the score matrix
# matrix:the user-movie matrix
# score_matrix:score matrix of movie for different users
# user:the user id
# n:the number of recommendations
def recommend(matrix, score_matrix, user, n):
    user_ratings = matrix.ix[user]
    not_rated_item = user_ratings[user_ratings == 0]
    recom_items = {}
    # recom_items={'a':1,'b':7,'c':3}
    for item in not_rated_item.index:
        recom_items[item] = score_matrix[item][user]
    recom_items = pd.Series(recom_items)
    recom_items = recom_items.sort_values(ascending=False)
    return recom_items[:n]


# main
score_matrix = cal_matscore(mdata, mcors)
with open("re_result.csv","w") as f:
    writer = csv.writer(f)
    for i in username:
        user = i
        print(user)
        print(recommend(mdata, score_matrix, user, 2))
        # s = recommend(mdata, score_matrix, user, 2)
        # s.index.name = user
        # s.to_csv("test.csv")
        # writer.writerows(s)
    print("end")
