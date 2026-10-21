"""
Filename: tree.py
Author: Bradley Cruthirds & James Durcan
Date: 2026-10-21
Description: Defines the Node and Tree classes.
"""

import random
import copy
import numpy as np
    

def generate_random_node(root=False, num_x_vals=1):
    """
    Generates a random node for the tree. If root is True, only operators are allowed. If root is False, both operators and operands are allowed.
    :param root: whether the node is the root of the tree or not
    :param num_x_vals: the number of x values to be used in the tree
    :return: the generated node
    """
    if root:
        allowed_values = ['+', '-', '*', '/']
    else:
        allowed_values = ['+', '-', '*', '/', 'x', 'x', 'x', 'x', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    node = Node(random.choice(allowed_values))
    if node.value == 'x':
        x_num = random.randint(1, num_x_vals)
        node.value = 'x' + str(x_num)
    if node.value in ['+', '-', '*', '/']:
        node.left = generate_random_node(num_x_vals=num_x_vals)
        node.right = generate_random_node(num_x_vals=num_x_vals)
    return node

class Node:
    """
    A class representing a node in a binary tree. Each node has a value, a left child, and a right child.
    """
    def __init__(self, value):
        """
        Initializes a Node with a given value. The left and right children are initialized to None.
        :param value: the value of the node
        """
        self.value = value
        self.left = None
        self.right = None

class Tree:
    """
    A class representing a binary tree. The tree has a root node and a fitness value. The tree can be mutated and crossed over with another tree.
    """
    def __init__(self, num_x_vals=1):
        """
        Initializes a Tree with a random root node. The fitness value is initialized to 0. The number of x values is set to the given value.
        :param num_x_vals: the number of x values from the dataset to be used in the tree
        """
        self.root = generate_random_node(root=True, num_x_vals=num_x_vals)
        self.fitness = 0
        self.num_x_vals = num_x_vals

    def clone(self):
        """
        Clones the tree by creating a deep copy of it.
        :return: the cloned tree
        """
        return copy.deepcopy(self)

    def mutate(self):
        """
        Mutates the tree by replacing a random node with a new randomly generated subtree.
        :return: the mutated tree
        """
        tree_copy = self.clone()
        rand_node = tree_copy.find_random_node()
        new_subtree = generate_random_node(num_x_vals=self.num_x_vals)
        rand_node.value = new_subtree.value
        rand_node.left = new_subtree.left
        rand_node.right = new_subtree.right

        return tree_copy

    def crossover(self, other_tree):
        """
        Performs crossover between this tree and another tree by replacing a random node in this tree with a random node from the other tree.
        :param other_tree: the other tree to crossover with
        :return: the new tree resulting from the crossover
        """
        new_tree1 = self.clone()
        newTree = other_tree.clone()
        tree1_rand = new_tree1.find_random_node()
        tree2_rand = newTree.find_random_node()

        tree1_rand.value = tree2_rand.value
        tree1_rand.left = tree2_rand.left
        tree1_rand.right = tree2_rand.right

        return new_tree1

    def find_random_node(self):
        """
        Finds a random node in the tree by generating a random number between 1 and the total number of nodes in the
        tree, and then traversing the tree to find the corresponding node.
        :return: The randomly selected node
        """
        baseNode = self.root
        num_nodes = self.count_num_nodes(baseNode)
        random_num = random.randint(1, num_nodes)
        return self.getNode(self.root, random_num)

    #Returns the tree evaluated given an x
    def get_fitness(self, x_vals):
        """
        Calculates the fitness of a random tree, evaluating the tree with the given x values.
        :param x_vals: a numpy array of x values to evaluate the tree with
        :return: the predicted y values from the tree evaluation
        """
        y_hats = self._get_fitness_helper(self.root, x_vals)
        return y_hats

    def _get_fitness_helper(self, node, x_vals):
        """
        Helper function to recursively evaluate the tree and calculate the predicted y values.
        :param node: the current node being evaluated
        :param x_vals: a numpy array of x values to evaluate the tree with
        :return: the predicted y values from the tree evaluation
        """
        if node.left is None and node.right is None:
            if "x" in node.value:
                x_index = int(node.value[1:]) - 1
                return x_vals[:, x_index]
            else:
                return float(node.value)

        left_val = self._get_fitness_helper(node.left, x_vals)
        right_val = self._get_fitness_helper(node.right, x_vals)

        if node.value == "+":
            return left_val + right_val
        elif node.value == "-":
            return left_val - right_val
        elif node.value == "*":
            return left_val * right_val
        elif node.value == "/":
            left_val = np.array(left_val, dtype=np.float64)
            right_val = np.array(right_val, dtype=np.float64)

            with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
                result = np.divide(
                    left_val, right_val, out=np.ones(np.broadcast_shapes(left_val.shape, right_val.shape)), where=np.abs(right_val) > 1e-8
                )

            return result

    def tree_to_string(self):
        """
        Converts the tree to a string representation.
        :return: the string representation of the tree
        """
        def traverse(node):
            if node is None:
                return ""
            return f"({traverse(node.left)} {node.value} {traverse(node.right)})"
        return traverse(self.root)

    def getNode(self, node, num):
        """
        Gets the node at the given position in the tree.
        :param node:
        :param num:
        :return:
        """
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
        """
        Counts the number of nodes in the tree.
        :param node: The current node being counted
        :return: the total number of nodes in the tree
        """
        count = 1
        if node.left:
            count = count + self.count_num_nodes(node.left)
        if node.right:
            count = count + self.count_num_nodes(node.right)
        return count



if __name__ == "__main__":
    tree = Tree(num_x_vals=2)
    string = tree.tree_to_string()
    print(tree.tree_to_string())
    print(tree.get_fitness([1,2]))

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