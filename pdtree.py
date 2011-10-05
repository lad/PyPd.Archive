#!/usr/bin/env python

""" A tree data structure oriented towards storing Pd objects. """

import collections
import pdtest

(CHILDREN_ONLY, DEPTH_FIRST, BREADTH_FIRST) = range(3)

class SimpleTree(object):
    """This simple tree abstraction dispenses with the notion of separate
       tree and node classes and uses a single class for both. All nodes
       in the tree are instances of Simpletree."""

    def __init__(self, value = None):
        (self.value, self._children) = (value, [])

    def __len__(self):
        return len(self._children)

    def __getitem__(self, i):
        if isinstance(i, slice):
            indices = i.indices(len(self._children))
            return [self._children[i] for i in range(*indices)]
            #raise NotImplementedError('PdTree does not support slices')
        return self._children[i]

    def add(self, value):
        tree = SimpleTree(value)
        self._children.append(tree)
        return tree

    def addTree(self, tree):
        self._children.append(tree)

    def insert(self, i, value):
        tree = SimpleTree(value)
        self._children.insert(i, tree)
        return tree

    def insertTree(self, i, tree):
        self._children.insert(i, tree)

    def iter(self, order):
        if order == CHILDREN_ONLY:
            return iter(self._children)
        elif order == DEPTH_FIRST:
            return self._depth_first_iter()
        elif order == BREADTH_FIRST:
            return self._breadth_first_iter()
        else:
            raise ValueError('Unknown order type: "%s"' % str(order))

    def _depth_first_iter(self):
        # The root node may be anonymous, if not yield it.
        if self.value is not None:
            yield self

        # Use a stack instead of recursion.
        child_stack = collections.deque(reversed(self._children))
        while True:
            try:
                child = child_stack.pop()
            except IndexError:
                # stack is empty, we're done...
                return

            yield child
            if child._children:
                child_stack.extend(reversed(child._children))

    def _breadth_first_iter(self):
        # The root node may be anonymous, if not yield it.
        if self.value is not None:
            yield self

        this_level = self._children

        while this_level:
            next_level = []
            for sib in this_level:
                yield sib
                if sib._children:
                    next_level.extend(sib._children)

            this_level = next_level

    def apply(self, order, fn):
        for node in self.iter(order):
            fn(node)

