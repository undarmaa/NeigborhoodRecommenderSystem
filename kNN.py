from numpy import *
import numpy as np
import data_io as dio
import csv
import pandas as pd

with open(dio.data_path + 'addr.csv', 'rb') as f1:
    next(f1)
    reader = csv.reader(f1, delimiter=',')
    trainSet = []
    labels = []
    for row in reader:
        trainSet.append([float(row[3]), float(row[4])])
        labels.append(int(float(row[1])))

    trainSet = np.asarray(trainSet)
    labels = np.asarray(labels)

with open(dio.data_path + 'dest.csv', 'rb') as f2:
    next(f2)
    reader1 = csv.reader(f2, delimiter=',')
    testSet = []
    name_no = []
    for row in reader1:
        name_no.append(int(float(row[1])))
        testSet.append([float(row[3]), float(row[4])])

    testSet = np.asarray(testSet)



def kNN_classifier(testData, trainSet, labels, k):

    trainSetSize = trainSet.shape[0]

    # euclidian distance
    diffMat = tile(testData, (trainSetSize, 1)) - trainSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5

    sortedDistIndicies = distances.argsort()

    return labels[sortedDistIndicies[0]], labels[sortedDistIndicies[1]]


df = pd.DataFrame(columns=['name_no', 'sigungu_no'])

j = 0
for i in range(len(testSet)):
    result = kNN_classifier(testSet[i], trainSet, labels, 2)
    #print i, name_no[i], result[0]
    df.loc[j] = [name_no[i], result[0]]
    j += 1
    #print i, name_no[i], result[1]
    df.loc[j] = [name_no[i], result[1]]
    j += 1

df.to_csv(dio.data_path + "nnfromdest.csv")





