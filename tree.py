import random
import copy
import operator
    

def generate_random_node(root=False):
    if root:
        allowed_values = ['+', '-', '*', '/']
    else:
        allowed_values = ['+', '-', '*', '/', 'x', 'x', 'x', 'x', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    node = Node(random.choice(allowed_values))
    if node.value in ['+', '-', '*', '/']:
        node.left = generate_random_node()
        node.right = generate_random_node()
    return node

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = generate_random_node(root=True)
        self.operationDict = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}

    def clone(self):
        return copy.deepcopy(self)

    def mutate(self):
        tree_copy = self.clone()
        rand_node = tree_copy.find_random_node()
        new_subtree = generate_random_node()
        rand_node.value = new_subtree.value
        rand_node.left = new_subtree.left
        rand_node.right = new_subtree.right

        return tree_copy

    def crossover(self, other_tree):
        new_tree1 = copy.deepcopy(self)
        tree1_rand = new_tree1.find_random_node()
        tree2_rand = other_tree.find_random_node()

        tree1_rand.value = tree2_rand.value
        tree1_rand.left = tree2_rand.left
        tree1_rand.right = tree2_rand.right

        return new_tree1

    def find_random_node(self):
        baseNode = self.root
        num_nodes = self.count_num_nodes(baseNode)
        random_num = random.randint(1, num_nodes)
        return self.getNode(self.root, random_num)

    def get_fitness(self, x):

        string = self.tree_to_string()
        return eval(string.replace("x", str(x)))

    def tree_to_string(self):
        def traverse(node):
            if node is None:
                return ""
            return f"({traverse(node.left)} {node.value} {traverse(node.right)})"
        return traverse(self.root)

    def getNode(self, node, num):
        myCount = 1
        if node.left:
            myCount = self.count_num_nodes(node.left) + 1
        if myCount == num:
            return node
        if num > myCount:
            return self.getNode(node.right, num-myCount)
        else:
            return self.getNode(node.left,num)


    def count_num_nodes(self, node):
        count = 1
        if node.left:
            count = count + self.count_num_nodes(node.left)
        if node.right:
            count = count + self.count_num_nodes(node.right)
        return count



if __name__ == "__main__":
    # tree = Tree()
    # string = tree.tree_to_string()
    # print(tree.tree_to_string())

    # new_tree = copy.deepcopy(tree)
    # new_tree.root.value = "/"
    # print(new_tree.tree_to_string())

    # tree2 = Tree()
    #
    # print(tree2.tree_to_string())
    #
    # rand1 = tree.root.left
    # rand2 = tree2.root.right
    #
    # rand1.value = rand2.value
    # rand1.left = rand2.left
    # rand1.right = rand2.right
    #
    # print(tree.tree_to_string())
    #
    # tree2.root.left.value = "!"
    #
    # print(tree2.tree_to_string())
    # print(tree.tree_to_string())

    # mutated_tree = tree.mutate()
    # print(mutated_tree.tree_to_string())

    # tree2 = Tree()
    # print(tree2.tree_to_string())
    # crossover = tree.crossover(tree2)
    # print(crossover.tree_to_string())

    dict = {"+": operator.add, "-": operator.sub}

    print(dict["-"](4,3))



