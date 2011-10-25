#!/usr/bin/env python

""" A simple tree data structure. This is oriented towards storing Pd objects
though does not have any actual dependency on the rest of the Pd code. There's
no need for this code to understand anything about Pd."""

import collections
import pdtest

# TODO
#
# Use weakref for child to parent links. Otherwise we have a circular reference
# which will cause Python to use Garbage Collection, rather than ref-counting
# which is much slower.

class SimpleTree(object):
    """This tree abstraction dispenses with the notion of separate tree and
    node classes and uses a single class for both. All nodes in the tree are
    instances of Simpletree."""

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
           of the node value, an integer indicating its level in the tree."""

        # Yield the root
        yield (self, 0)

        # Use a stack instead of recursion. Each tuple in the stack is a node
        # and its level in the tree.
        child_stack = collections.deque([(c, 1)  for c in \
                                         reversed(self._children)])
        while True:
            try:
                (child, level) = child_stack.pop()
            except IndexError:
                # stack is empty, we're done...
                return

            # Yield each node
            yield (child, level)

            if child._children:
                child_stack.extend([(c, level + 1) for c in \
                                    reversed(child._children)])

    def apply(self, fn):
        for (node, level) in self:
            fn(node, level)

