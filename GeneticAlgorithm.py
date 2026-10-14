import csv
import random
from tree import Tree
from sklearn.metrics import mean_squared_error

def getData():
    DATASETS = ["dataset1.csv", "dataset2.csv", "dataset3.csv"]
    listsOfData = []

    for i in range(len(DATASETS)):

        dataList = []
        with open(DATASETS[i], newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                dataList.append(tuple(row))

        dataList.pop(0)
        listsOfData.append(dataList)
    return listsOfData

def getTrainTest(dataList, testSize):

    middle = dataList.copy()
    random.shuffle(middle)
    test = middle[:testSize]
    train = middle[testSize:]


    return train, test

#This will only work for the 1 x version. Can change later with an override if len(dataset[0]) > 1
def trueFitness(tree, dataset):
    ys = []
    y_predicted = []
    for row in dataset:
        ys.append(row[1])
        y_predicted.append(tree.get_fitness(float(row[0])))
    return mean_squared_error(ys, y_predicted)


        

    return

dataList = getData()

dataSet1 = dataList[0]

myTree = Tree()
print(myTree.tree_to_string())
print(trueFitness(myTree, dataSet1))





