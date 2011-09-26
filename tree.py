#!/usr/bin/env python

""" Simple tree data structure for storing PD objects. """

class Tree:
    """ This could be a generic tree structure, but is oriented towards storing
        objects from PD patch files. It allows the caller to specify which
        nodes have children, when they are created (addLeaf vs. addBranch).
        This is useful since the vast majority of nodes in the tree will be
        leaves.  Only sub-patches (i.e. canvas) objects have children. """

    def __init__(self, node):
        self._node = node
        self._children = []

    def applyDF(self, fn, tree = None):
        """Apply the given callable to all nodes in the tree depth first."""

        if tree is None:
            tree = self

        fn(tree._node)
        for c in tree._children:
            # Normally I think isinstance is a bad idea. It should probably
            # only be used for simple cases like this.
            if isinstance(c, Tree):
                self.applyDF(fn, tree = c)
            else:
                fn(c)

    def addLeaf(self, node):
        self._children.append(node)

    def addBranch(self, node):
        t = Tree(node)
        self._children.append(t)
        return t
