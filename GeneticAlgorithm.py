import csv
import random
from tree import Tree
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

##PAY ATTENTION HERE##
#Biggest problem is that we will get something good and it will go away

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

#Punishing largeness would probably be done in here - use method countnumnodes
def fitness_to_weights(population, dataset):
    for tree in population:
        tree.fitness = trueFitness(tree, dataset)
    fitnesses = [t.fitness for t in population]
    largest = max(fitnesses)
    weights = [largest - f for f in fitnesses]
    return weights

def makeTrees(numTrees):
    trees = []
    for i in range(numTrees):
        trees.append(Tree())
    return trees

#Obviously these should be changed to be as good as possible
#This one is insane but i wanted to leave it running so im pushing with it
NUM_GENS = 1000
MUTATION_PROB = 0.02
CROSSOVER_PROB = 0.1
POPULATION_SIZE = 500


dataList = getData()
dataSet1 = dataList[0]
current_gen = makeTrees(POPULATION_SIZE)
best = []

i = 0
for i in range(NUM_GENS):
    next_gen = []
    weights = fitness_to_weights(current_gen, dataSet1)
    # populate next generation
    for j in range(POPULATION_SIZE):
        #This breaks when all fitness are the same (like can happen if we do really good)
        #Should make a break in that case
        parent1 = random.choices(current_gen, weights)[0]
        flip = random.random()
        if flip <= MUTATION_PROB:  # mutation
            next_gen.append(parent1.mutate())
        elif flip <= CROSSOVER_PROB + MUTATION_PROB:  # crossover
            parent2 = random.choices(current_gen, weights)[0]
            next_gen.append(parent1.crossover(parent2))
        else:  # clone
            next_gen.append(parent1)
            
    # remember the best individual in this generation
    best_tour = min(current_gen, key=lambda t: t.fitness)
    best.append(best_tour)
    
    # reset the current gen
    current_gen = next_gen

for i in range(len(best)):
    print(i, best[i].tree_to_string(), best[i].fitness)

plt.plot(range(NUM_GENS), [t.fitness for t in best], 'rx-')
plt.show()







