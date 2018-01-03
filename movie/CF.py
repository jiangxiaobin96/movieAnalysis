# coding: utf-8
import sys
import numpy as np
import pandas as pd
from numpy import linalg as la

index_user = {}
re_index_user = {}
iuser = 0
index_movie = {}
re_index_movie = {}
imovie = 0
topuser = set()
users = 0
movies = 0
Edge = []


def get_index_user(x):
    global iuser
    if x in index_user:
        return index_user[x]
    else:
        index_user[x] = iuser
        re_index_user[iuser] = x
        iuser += 1
        return index_user[x]


def get_index_movie(x):
    global imovie
    if x in index_movie:
        return index_movie[x]
    else:
        index_movie[x] = imovie
        re_index_movie[imovie] = x
        imovie += 1
        return index_movie[x]


def cosSim(inA, inB):
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * (num / denom)


def SVD(dataMat):
    dataMat = np.mat(dataMat)
    U, Sigma, VT = la.svd(dataMat)
    Sig4 = np.mat(np.eye(4) * Sigma[:4])  # arrange Sig4 into a diagonal matrix
    xformedItems = dataMat.T * U[:, :4] * Sig4.I  # create transformed items
    return xformedItems


def get_sim():
    global users
    global movies
    SIM = np.zeros((users, movies))
    for i in range(users):
        for j in range(movies):
            SIM[i][j] = cosSim(xformedItems[i, :].T, xformedItems[j, :].T)
    return SIM


def svdEst(dataMat, user, simMeas, item, SIM):
    simTotal = 0.0
    ratSimTotal = 0.0
    for i in range(len(Edge[user])):
        j = Edge[user][i]
        userRating = dataMat[user, j]
        if userRating == 0 or j == item: continue
        similarity = SIM[j, item]
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def recommend(SIM, dataMat, user, simMeas=cosSim, estMethod=svdEst):
    dataMat = np.mat(dataMat)
    unratedItems = np.nonzero(dataMat[user, :].A == 0)[1]
    itemScores = []
    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item, SIM)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)


def read_review():
    temp = []
    global movies
    movie = set()

    with open('review.txt', 'r') as f:
        for line in f.readlines():
            x = line.split('\t')
            temp.append(x)
            movie.add(x[0])
    movies = len(movie)
    dataMat = np.zeros((users, movies))
    for i in range(movies): Edge.append([]);

    for i in range(len(temp)):
        if temp[i][1] in topuser:
            dataMat[int(get_index_user(temp[i][1]))][int(get_index_movie(temp[i][0]))] = int(temp[i][2])
            Edge[int(get_index_user(temp[i][1]))].append(int(get_index_movie(temp[i][0])))
    return dataMat


def read_top():
    global users
    with open('top reviewers.txt', 'r') as f:
        for line in f.readlines():
            topuser.add(line.split('\t')[0])
    users = len(topuser)


if __name__ == "__main__":
    read_top()
    dataMat = read_review()
    print(re_index_user[321])
    xformedItems = SVD(dataMat)
    print("SVD has been done")
    SIM = get_sim()
    print("SIM  matrix has been done")
    REC = recommend(SIM, dataMat, 321)
    for i in range(0, 5):
        print(re_index_movie[int(REC[i][0])])
