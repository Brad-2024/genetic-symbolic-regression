import random
import copy
import operator
    

def generate_random_node(root=False):
    if root:
        allowed_values = ['+', '-', '*', '/']
    else:
        allowed_values = ['+', '-', '*', '/', 'x1', 'x1', 'x2', 'x2', 'x3', 'x3', '1', '2', '3', '4', '5', '6', '7', '8', '9']
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

#Operation dict allows us to convert string values into operations
_OPERATIONDICT = {
    "+": operator.add, 
    "-": operator.sub, 
    "*": operator.mul, 
    "/": operator.truediv
}

class Tree:
    def __init__(self):
        self.root = generate_random_node(root=True)
        self.fitness = 0

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
        new_tree1 = self.clone()
        newTree = other_tree.clone()
        tree1_rand = new_tree1.find_random_node()
        tree2_rand = newTree.find_random_node()

        tree1_rand.value = tree2_rand.value
        tree1_rand.left = tree2_rand.left
        tree1_rand.right = tree2_rand.right

        return new_tree1

    def find_random_node(self):
        baseNode = self.root
        num_nodes = self.count_num_nodes(baseNode)
        random_num = random.randint(1, num_nodes)
        return self.getNode(self.root, random_num)

    #Returns the tree evaluated given an x
    def get_fitness(self, x1, x2, x3):
        return self._get_fitness_helper(self.root, x1, x2, x3)

    def _get_fitness_helper(self, node, x1, x2, x3):
        if node.value not in _OPERATIONDICT.keys():
            if node.value == 'x1':
                return x1
            elif node.value == 'x2':
                return x2
            elif node.value == 'x3':
                return x3
            else:
                return float(node.value)
        else:
            right = self._get_fitness_helper(node.right, x1, x2, x3)
            if right == 0 and node.value == '/':
                return 0
            return _OPERATIONDICT[node.value](self._get_fitness_helper(node.left, x1, x2, x3), right)

    #Returns human readable (kinda) equation
    def tree_to_string(self):
        def traverse(node):
            if node is None:
                return ""
            return f"({traverse(node.left)} {node.value} {traverse(node.right)})"
        return traverse(self.root)

    #Gets node based on number in tree
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

    #Counts total number of nodes in tree
    def count_num_nodes(self, node):
        count = 1
        if node.left:
            count = count + self.count_num_nodes(node.left)
        if node.right:
            count = count + self.count_num_nodes(node.right)
        return count



if __name__ == "__main__":
    tree = Tree()
    string = tree.tree_to_string()
    print(tree.tree_to_string())
    print(tree.get_fitness(1))

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