#!/usr/bin/env python

""" A tree data structure oriented towards storing Pd objects. """

import collections
import pdtest

class SimpleTree(object):
    """This simple tree abstraction dispenses with the notion of separate
       tree and node classes and uses a single class for both. All nodes
       in the tree are instances of Simpletree."""

    def __init__(self, value = None, parent = None):
        (self.parent, self.value, self._children) = (parent, value, [])

    def __len__(self):
        return len(self._children)

    def __getitem__(self, i):
        if isinstance(i, slice):
            indices = i.indices(len(self._children))
            return [self._children[i] for i in range(*indices)]
        else:
            return self._children[i]

    def add(self, value):
        tree = SimpleTree(value, parent = self)
        self._children.append(tree)
        return tree

    def addBranch(self, tree):
        tree.parent = self
        self._children.append(tree)

    def insert(self, i, value):
        tree = SimpleTree(value, parent = self)
        self._children.insert(i, tree)
        return tree

    def insertBranch(self, i, tree):
        tree.parent = self
        self._children.insert(i, tree)

    def leaf(self):
        return self._children == []

    def __iter__(self):
        """Iteration is depth first as this is the only order that makes sense
           for a Pd patch. Each object is yielded in the order it appears in
           the original patch.  Each value yielded by the iterator is a tuple
           of the node value, the object-id, and an integer indicating its
           level in the tree."""

        # The object ids must be generated dynamically, as they change when
        # the tree is modified. The root node is given the id of -1, as Pd
        # root objects (canvas objects) don't actually have an id in Pd
        # parlance.
        obj_id = -1

        # Yield the root
        yield (self, obj_id, 0)

        # Use a stack instead of recursion. Each tuple in the stack is a node
        # and its level in the tree.
        child_stack = collections.deque([(c, 1)  for c in \
                                         reversed(self._children)])
        # Need to keep track of the object id as we move up and down levels
        # in the tree
        obj_id_stack = collections.deque()

        last_level = 1
        while True:
            try:
                (child, level) = child_stack.pop()
            except IndexError:
                # stack is empty, we're done...
                return

            # Work out the object-id
            if level == last_level:
                obj_id += 1
            elif level == (last_level - 1):
                obj_id = obj_id_stack.pop() + 1
            elif level == (last_level + 1):
                obj_id = 0
            last_level = level

            # Yield each node
            yield (child, obj_id, level)

            if child._children:
                child_stack.extend([(c, level + 1) for c in \
                                    reversed(child._children)])
                obj_id_stack.append(obj_id)
                obj_id = -1

    def apply(self, fn):
        for (node, level) in self:
            fn(node, level)

