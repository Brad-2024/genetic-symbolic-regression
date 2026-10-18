import csv
import random
from tree import Tree
import sklearn
import matplotlib.pyplot as plt

##PAY ATTENTION HERE##
#Biggest problem is that we will get something good and it will go away
#Good bloat paper https://link.springer.com/content/pdf/10.1023/A:1010024515191.pdf

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

#This will only work for the 1 x version. Can change later with an override if len(dataset[0]) > 2
#Lowkey, traversing and doing calcs on the tree might not be the fastest way. can we simplify and then switch X out?
def trueFitness(tree, dataset, num_x_vals=1):
    ys = []
    y_predicted = []
    for row in dataset:
        ys.append(row[num_x_vals])
        y_predicted.append(tree.get_fitness([float(x) for x in row[:num_x_vals]]))
    return sklearn.metrics.mean_squared_error(ys, y_predicted)

#Punishing largeness would probably be done in here - use method countnumnodes
def fitness_to_weights(population, dataset):
    for tree in population:
        tree.fitness = trueFitness(tree, dataset)
        #Just random ass numbers bro
        numberNodes = tree.count_num_nodes(tree.root)
        if numberNodes > 15:
            tree.fitness = tree.fitness + (numberNodes-15)**1.25
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
NUM_GENS = 500
MUTATION_PROB = 0.02
CROSSOVER_PROB = 0.1
POPULATION_SIZE = 250


dataList = getData()
dataSet1 = dataList[0]
# dataSet1, TestSet = sklearn.model_selection.train_test_split(firstSet, test_size=0.2)
current_gen = makeTrees(POPULATION_SIZE)
best = []

try:
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
        print(f"gen {i} finished")

except KeyboardInterrupt:
    print("Interrupted; showing results from completed generations.")

if best:
    for i in range(len(best)):
        print(i, best[i].tree_to_string(), best[i].fitness)

    plt.plot(range(len(best)), [t.fitness for t in best], 'rx-')
    plt.show()







