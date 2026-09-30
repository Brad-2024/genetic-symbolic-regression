import csv
import random

DATASETS = ["dataset1.csv", "dataset2.csv", "dataset3.csv"]

def getTrainTest(dataList, testSize):

    middle = dataList.copy()
    random.shuffle(middle)
    test = middle[:testSize]
    train = middle[testSize:]


    return train, test


listsOfData = []

for i in range(len(DATASETS)):

    dataList = []
    with open(DATASETS[i], newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            dataList.append(tuple(row))

    dataList.pop(0)
    listsOfData.append(dataList)


