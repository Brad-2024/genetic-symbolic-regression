import random


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

    def mutate(self):
        pass

    def crossover(self, other_tree):
        pass

    def get_fitness(self):
        pass

    def tree_to_string(self):
        def traverse(node):
            if node is None:
                return ""
            return f"({traverse(node.left)} {node.value} {traverse(node.right)})"
        return traverse(self.root)


if __name__ == "__main__":
    tree = Tree()
    string = tree.tree_to_string()

    print(string)
    print(string.replace("x", "1"))
    print(eval(string.replace("x", "1")))

