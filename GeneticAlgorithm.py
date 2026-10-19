import csv
import random
from tree import Tree
import sklearn
import matplotlib.pyplot as plt
import numpy as np

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
def trueFitness(tree, dataset, num_x_vals=1, dataset_num=1):
    xs = dataset[:, :num_x_vals]
    ys = dataset[:, num_x_vals]

    y_predicted = tree.get_fitness(xs)
    y_predicted = np.broadcast_to(y_predicted, ys.shape)

    if not np.all(np.isfinite(y_predicted)):
        return float('inf')

    if dataset_num == 1:
        return np.mean((ys - y_predicted) ** 2)
    elif dataset_num == 2:
        return np.mean(np.abs(ys - y_predicted) / (np.abs(ys) + 1))

def calculate_fitness(population, dataset, dataset_num=1):
    for tree in population:
        tree.fitness = trueFitness(
            tree, dataset, num_x_vals=tree.num_x_vals, dataset_num=dataset_num
        )

        numberNodes = tree.count_num_nodes(tree.root)

        if numberNodes > 15:
            tree.fitness += 0.001 * (numberNodes - 15) ** 1.25


def tournament_selection(population, tournament_size=3):
    competitors = random.sample(population, tournament_size)
    return min(competitors, key=lambda t: t.fitness)

def makeTrees(numTrees, num_x_vals=1):
    trees = []
    for i in range(numTrees):
        trees.append(Tree(num_x_vals=num_x_vals))
    return trees


def scale_features(dataset, num_x_vals):
    dataset = dataset.copy()

    scales = []

    for i in range(num_x_vals):
        x = dataset[:, i]

        median_magnitude = np.median(np.abs(x))

        if median_magnitude > 0:
            scale = 10 ** np.floor(np.log10(median_magnitude))
        else:
            scale = 1.0

        dataset[:, i] /= scale
        scales.append(scale)

    return dataset, scales

#Obviously these should be changed to be as good as possible
#This one is insane but i wanted to leave it running so im pushing with it
dataList = getData()
dataSet1 = dataList[0]
# make dataset1 a numpy array of floats
dataSet1 = np.array(dataSet1, dtype=float)
dataSet2 = dataList[1]
# make dataset2 a numpy array of floats
dataSet2 = np.array(dataSet2, dtype=float)
dataSet2, scales = scale_features(dataSet2, num_x_vals=3)

print("Scaling factors:", scales)

NUM_GENS = 50
MUTATION_PROB = 0.2
CROSSOVER_PROB = 0.3
POPULATION_SIZE = 50
num_x_vals = 1


dataList = getData()
dataSet1 = dataList[0]
dataSet2 = dataList[1]
# dataSet1, TestSet = sklearn.model_selection.train_test_split(firstSet, test_size=0.2)
current_gen = makeTrees(POPULATION_SIZE, num_x_vals=num_x_vals)
best = []

try:
    for i in range(NUM_GENS):
        calculate_fitness(current_gen, dataset, dataset_num=dataset_num)

        elite = min(current_gen, key=lambda t: t.fitness)

        next_gen = [elite]

        rand_num = int(POPULATION_SIZE * 0.10)
        # populate next generation
        for j in range(POPULATION_SIZE - 1 - rand_num):
            #This breaks when all fitness are the same (like can happen if we do really good)
            #Should make a break in that case
            parent1 = tournament_selection(current_gen)
            flip = random.random()
            if flip <= MUTATION_PROB:  # mutation
                next_gen.append(parent1.mutate())
            elif flip <= CROSSOVER_PROB + MUTATION_PROB:  # crossover
                parent2 = tournament_selection(current_gen)
                next_gen.append(parent1.crossover(parent2))
            else:  # clone
                next_gen.append(parent1)

        next_gen.extend(makeTrees(rand_num, num_x_vals=num_x_vals))
                
        # remember the best individual in this generation
        best_tour = min(current_gen, key=lambda t: t.fitness)
        best.append(best_tour)
        print("Fitness:", best_tour.fitness)

        print("Raw MSE:", trueFitness(best_tour, dataSet1, num_x_vals=num_x_vals))

        print("Nodes:", best_tour.count_num_nodes(best_tour.root))
        
        # reset the current gen
        current_gen = next_gen
        print(f"gen {i} finished")

except KeyboardInterrupt:
    print("Interrupted; showing results from completed generations.")

if best:
    for i in range(len(best)):
        if dataset_num == 2:
            equation_string = best[i].tree_to_string()
            for j in range(num_x_vals):
                equation_string = equation_string.replace(f"x{j+1}", f"(x{j+1}/{scales[j]})")
            print(i, equation_string, best[i].fitness)
        else:
            print(i, best[i].tree_to_string(), best[i].fitness)

    plt.plot(range(len(best)), [t.fitness for t in best], 'rx-')
    plt.show()







