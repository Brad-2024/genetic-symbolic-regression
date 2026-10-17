import csv
import random
# from tree import Tree
from MultiValTree import Tree
import sklearn
import matplotlib.pyplot as plt
import math

##PAY ATTENTION HERE##
#Biggest problem is that we will get something good and it will go away
#Good bloat paper https://link.springer.com/content/pdf/10.1023/A:1010024515191.pdf

#ToDo#
#Get dataset3 setup
#Make script for testing hyperparameters
#Actually check for bloat
#Do the crossover from the paper
#Find more good papers on what to do 
#Maybe a good seed Population
#Train test split

#ToDo if time allows/if struggling
#Have a diversity checker

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
def trueFitness(tree, dataset):
    y_predicted = []
    if(len(dataset[0]) == 2):
        for row in dataset:
            y_predicted.append(tree.get_fitness(float(row[0])), 2)
    elif(len(dataset[0]) == 4):
        for row in dataset:
            y_predicted.append(round(tree.get_fitness(float(row[0]), float(row[1]), float(row[2])), 2))
    # return sklearn.metrics.mean_squared_error(ys, y_predicted)
    return sklearn.metrics.mean_absolute_error(ys, y_predicted)
    
#Punishing largeness would probably be done in here - use method countnumnodes
def fitness_to_weights(population, dataset):
    for tree in population:
        tree.fitness = trueFitness(tree, dataset)
        #Just random ass numbers bro
        numberNodes = tree.count_num_nodes(tree.root)
        if numberNodes > 20:
            tree.fitness = tree.fitness + (numberNodes-20)**1.5
    fitnesses = [t.fitness for t in population]
    #This worked for 1 where there werent as many outliers i 
    # largest = max(fitnesses)
    # weights = [largest - f for f in fitnesses]
    #Log didnt help much
    # largest = math.log(max(fitnesses))
    # weights = [largest - math.log(f) for f in fitnesses]
    order = sorted(range(len(population)), key=lambda i: fitnesses[i])
    weights = [0.0] * len(population)

    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and fitnesses[order[end]] == fitnesses[order[start]]:
            end += 1

        # Give tied fitnesses the average weight for their rank positions.
        average_weight = len(population) - (start + end - 1) / 2
        for position in range(start, end):
            weights[order[position]] = average_weight

        start = end

    return weights

def makeTrees(numTrees):
    trees = []
    for i in range(numTrees):
        trees.append(Tree())
    return trees

#Obviously these should be changed to be as good as possible
#This one is insane but i wanted to leave it running so im pushing with it
NUM_GENS = 2000
MUTATION_PROB = 0.2
CROSSOVER_PROB = 0.2
POPULATION_SIZE = 500


dataList = getData()
dataSet1 = dataList[1]
# dataSet1, TestSet = sklearn.model_selection.train_test_split(firstSet, test_size=0.2)
current_gen = makeTrees(POPULATION_SIZE)
ys = []

if(len(dataSet1[0]) == 2):
    for row in dataSet1:
        ys.append(row[1])
elif len(dataSet1[0]) == 4:
    for row in dataSet1:
        ys.append(row[3])

    
best = []

try:
    for i in range(NUM_GENS):
        next_gen = []
        weights = fitness_to_weights(current_gen, dataSet1)
        # populate next generation
        best_tour = min(current_gen, key=lambda t: t.fitness)
        next_gen.append(best_tour)
        for j in range(POPULATION_SIZE-1):
            parent1 = random.choices(current_gen, weights)[0]
            flip = random.random()
            if flip <= MUTATION_PROB:  # mutation
                next_gen.append(parent1.mutate())
            elif flip <= CROSSOVER_PROB + MUTATION_PROB:  # crossover
                parent2 = random.choices(current_gen, weights)[0]
                # next_gen.append(parent1.crossover(parent2))
                next_gen.append(parent1.size_fair_crossover(parent2))
            else:  # clone
                next_gen.append(parent1.clone())
                
        # remember the best individual in this generation
        best.append(best_tour)
        
        # reset the current gen
        current_gen = next_gen
        unique_trees = len({tree.tree_to_string() for tree in current_gen})
        print(f"gen {i} finished. {unique_trees} different trees. Best fitness: {best_tour.fitness}.")
        print(best_tour.tree_to_string())
        if(best_tour.fitness<1):
            print("Candidate found: " + best_tour.tree_to_string())

except KeyboardInterrupt:
    print("Interrupted. Showing results from completed generations.")

# except ValueError:
#     print("Converged trees. Showing results so far.")

if best:
    for i in range(len(best)):
        print(i, best[i].tree_to_string(), best[i].fitness)

    plt.plot(range(len(best)), [t.fitness for t in best], 'rx-')
    plt.show()







