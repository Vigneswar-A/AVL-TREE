
from collections import deque


class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.height = 1
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.val)


class Tree:
    def __init__(self):
        self.root = None

    def get_height(node):
        if node is None:
            return 0
        return node.height

    def insert(self, val):
        def helper(node):
            if node is None:
                return Node(val)

            if val < node.val:
                node.left = helper(node.left)
            else:
                node.right = helper(node.right)

            node.height = max(Tree.get_height(node.left),
                              Tree.get_height(node.right)) + 1

            balance = Tree.get_balance(node)

            if balance > 1 and val < node.left.val:
                return Tree.rotate_right(node)

            if balance < -1 and val > node.right.val:
                return Tree.rotate_left(node)

            if balance > 1 and val > node.left.val:
                node.left = Tree.rotate_left(node.left)
                return Tree.rotate_right(node)

            if balance < -1 and val < node.right.val:
                node.right = Tree.rotate_right(node.right)
                return Tree.rotate_left(node)

            return node

        self.root = helper(self.root)

    def search(self, val):
        def helper(root):
            if root is None:
                return None

            if val < root.val:
                return helper(root.left)
            elif val > root.val:
                return helper(root.right)
            else:
                return root

        return helper(self.root)

    def delete(self, val):
        def helper(node, val):
            if not node:
                return None
            if node.val == val:
                if node.left and node.right:
                    temp = node.right
                    while temp.left:
                        temp = temp.left
                    node.val = temp.val
                    node.right = helper(node.right, temp.val)
                    return node

                return node.left or node.right

            if val < node.val:
                node.left = helper(node.left, val)
            else:
                node.right = helper(node.right, val)

            balance = Tree.get_balance(node)

            if balance > 1 and Tree.get_balance(node.left) >= 0:
                return Tree.rotate_right(node)

            if balance < -1 and Tree.get_balance(node.right) <= 0:
                return Tree.rotate_left(node)

            if balance > 1 and Tree.get_balance(node.left) <= 0:
                node.left = Tree.rotate_left(node.left)
                return Tree.rotate_right(node)

            if balance < -1 and Tree.get_balance(node.right) >= 0:
                node.right = Tree.rotate_right(node.right)
                return Tree.rotate_left(node)

            node.height = max(Tree.get_height(node.left),
                              Tree.get_height(node.right)) + 1

            return node

        self.root = helper(self.root, val)

    def get_balance(node):
        return Tree.get_height(node.left) - Tree.get_height(node.right)

    def rotate_right(node):
        other = node.left
        temp = other.right

        other.right = node
        node.left = temp

        node.height = max(Tree.get_height(node.left),
                          Tree.get_height(node.right)) + 1

        other.height = max(Tree.get_height(other.left),
                           Tree.get_height(other.right)) + 1

        return other

    def rotate_left(node):
        other = node.right
        temp = other.left

        other.left = node
        node.right = temp

        node.height = max(Tree.get_height(node.left),
                          Tree.get_height(node.right)) + 1

        other.height = max(Tree.get_height(other.left),
                           Tree.get_height(other.right)) + 1

        return other

    def level_order(self):
        if self.root is None:
            return None
        res = []
        prev = [self.root]
        n = 0
        while any(node != None for node in prev):
            n += 1
            temp = [None]*(2**n)
            for i in range(n):
                if prev[i] is None:
                    temp[2*i] = None
                    temp[2*i+1] = None
                else:
                    temp[2*i] = prev[i].left
                    temp[2*i+1] = prev[i].right
            res.append(prev)
            prev = temp
        return res

    def __str__(self):
        width = 2**(self.root.height) - 1
        tree_string = ""
        for level in self.level_order():
            tree_string += f'{" ".join(str(node.val) if node else "#" for node in level): ^{width}}\n'
        return tree_string


tree = Tree()
tree.insert(7)
tree.insert(2)
tree.insert(5)
tree.insert(9)
tree.insert(10)

print(tree)
tree.delete(5)
print(tree)
